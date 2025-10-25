from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.core.permissions import (
    can_customize_lunchbox,
    can_add_lunchbox_to_profile,
    PermissionDenied
)
from app.db.schemas.lunchbox import (
    LoncheraCreate, LoncheraRead, LoncheraUpdate,
    LoncheraItemCreate, LoncheraItemUpdate, LoncheraItemRead
)
from app.db.schemas.detail import LunchboxDetailFull
from app.db.models.core_models import Usuario
from app.crud import lunchbox as crud
from app.crud import detail as detail_crud
from app.services.restriction_validator import (
    check_food_against_restrictions,
    validate_lunchbox_foods,
    RestrictionViolation
)

router = APIRouter(prefix="/lunchboxes", tags=["lunchboxes"])


@router.get("/", response_model=list[LoncheraRead], summary="Listar loncheras")
def list_lunchboxes(hijo_id: int | None = None, db: Session = Depends(get_db)):
    """✅ TODOS pueden listar loncheras (filtradas por hijo si se especifica)"""
    return crud.list_(db, hijo_id=hijo_id)


@router.get("/{lunchbox_id}", response_model=LoncheraRead, summary="Obtener una lonchera")
def get_lunchbox(lunchbox_id: int, db: Session = Depends(get_db)):
    """✅ TODOS pueden ver una lonchera específica"""
    obj = crud.get_by_id(db, lunchbox_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    return obj


@router.get("/{lunchbox_id}/items", response_model=list[LoncheraItemRead], summary="Listar items de una lonchera")
def list_lunchbox_items(lunchbox_id: int, db: Session = Depends(get_db)):
    """✅ TODOS pueden ver los items de una lonchera"""
    return crud.list_items(db, lunchbox_id)


@router.get("/{lunchbox_id}/detail", response_model=LunchboxDetailFull, summary="Detalle completo con nutrición")
def get_lunchbox_detail(lunchbox_id: int, db: Session = Depends(get_db)):
    """
    ✅ TODOS pueden ver detalle completo
    Retorna: hijo, items, dirección, nutrición total, alertas
    """
    data = detail_crud.get_lunchbox_detail_full(db, lunchbox_id)
    if not data:
        raise HTTPException(status_code=404, detail="No encontrado")
    return data


@router.post("/", response_model=LoncheraRead, status_code=status.HTTP_201_CREATED, summary="Crear lonchera")
def create_lunchbox(
        payload: LoncheraCreate,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ⚠️ CONTROL DE PERMISOS:
    - Básico: Solo puede VER menús predeterminados (no crear)
    - Estándar: Puede agregar loncheras predeterminadas
    - Premium: Puede crear loncheras personalizadas
    """
    # Validar que el usuario tenga permiso para crear loncheras
    if not can_add_lunchbox_to_profile(current_user):
        raise PermissionDenied(
            "Tu plan actual no permite crear loncheras. "
            "Actualiza a Estándar o Premium para usar esta funcionalidad."
        )

    try:
        return crud.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{lunchbox_id}", response_model=LoncheraRead, summary="Actualizar lonchera")
def update_lunchbox(
        lunchbox_id: int,
        payload: LoncheraUpdate,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ⚠️ Actualizar fecha, estado o dirección de lonchera
    Estándar y Premium pueden actualizar
    """
    if not can_add_lunchbox_to_profile(current_user):
        raise PermissionDenied("No tienes permisos para actualizar loncheras")

    obj = crud.get_by_id(db, lunchbox_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")

    try:
        return crud.update(db, obj, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{lunchbox_id}/items", status_code=status.HTTP_201_CREATED, summary="Agregar alimento a lonchera")
def add_item(
        lunchbox_id: int,
        item: LoncheraItemCreate,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ⚠️ PERSONALIZACIÓN ALIMENTO POR ALIMENTO

    Privilegios:
    - Premium: Puede personalizar (agregar alimentos individuales)
    - Estándar: Solo puede usar loncheras predeterminadas
    - Básico: No puede modificar

    ✅ VALIDACIÓN DE RESTRICCIONES AUTOMÁTICA
    """
    # Validar permisos de personalización
    if not can_customize_lunchbox(current_user):
        raise PermissionDenied(
            "La personalización alimento por alimento requiere plan Premium. "
            f"Tu plan actual: {current_user.membresia.tipo if current_user.membresia else 'Ninguno'}"
        )

    # Obtener lonchera para saber el hijo_id
    lonchera = crud.get_by_id(db, lunchbox_id)
    if not lonchera:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")

    # 🔥 VALIDAR RESTRICCIONES ALIMENTARIAS
    es_permitido, mensaje_error = check_food_against_restrictions(
        db,
        lonchera.hijo_id,
        item.alimento_id
    )

    if not es_permitido:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "restriction_violation",
                "message": mensaje_error,
                "alimento_id": item.alimento_id,
                "hijo_id": lonchera.hijo_id
            }
        )

    try:
        crud.add_item(db, lunchbox_id, item)
        return {"ok": True, "message": "Alimento agregado correctamente"}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{lunchbox_id}/items/{alimento_id}", status_code=status.HTTP_200_OK, summary="Actualizar cantidad")
def update_item(
        lunchbox_id: int,
        alimento_id: int,
        payload: LoncheraItemUpdate,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """⚠️ Solo Premium puede actualizar cantidades (requiere personalización)"""
    if not can_customize_lunchbox(current_user):
        raise PermissionDenied("Solo usuarios Premium pueden modificar cantidades")

    try:
        crud.update_item(db, lunchbox_id, alimento_id, payload)
        return {"ok": True}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{lunchbox_id}/items/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Quitar alimento")
def remove_item(
        lunchbox_id: int,
        alimento_id: int,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ⚠️ Quitar alimento de lonchera
    - Premium: Puede quitar individualmente
    - Estándar: Solo puede eliminar lonchera completa predeterminada
    """
    if not can_customize_lunchbox(current_user):
        raise PermissionDenied(
            "Solo usuarios Premium pueden quitar alimentos individuales. "
            "Los usuarios Estándar deben eliminar la lonchera completa."
        )

    try:
        crud.remove_item(db, lunchbox_id, alimento_id)
        return
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{lunchbox_id}/validate", summary="Validar restricciones de lonchera")
def validate_lunchbox_restrictions(lunchbox_id: int, db: Session = Depends(get_db)):
    """
    ✅ Endpoint para validar si una lonchera cumple con restricciones del hijo

    Retorna:
    - is_valid: bool
    - errors: lista de mensajes de error
    - warnings: alertas nutricionales
    """
    lonchera = crud.get_by_id(db, lunchbox_id)
    if not lonchera:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")

    # Obtener items de la lonchera
    items = crud.list_items(db, lunchbox_id)
    alimentos_ids = [item.alimento_id for item in items]

    # Validar restricciones
    es_valida, errores = validate_lunchbox_foods(db, lonchera.hijo_id, alimentos_ids)

    return {
        "lunchbox_id": lunchbox_id,
        "hijo_id": lonchera.hijo_id,
        "is_valid": es_valida,
        "errors": errores if not es_valida else [],
        "total_items": len(items)
    }