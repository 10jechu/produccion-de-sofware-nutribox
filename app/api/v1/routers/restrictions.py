from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.core.permissions import can_configure_restrictions, PermissionDenied
from app.db.schemas.restriction import RestriccionCreate, RestriccionRead, RestriccionUpdate
from app.db.models.core_models import Usuario
from app.crud import restriction as crud

router = APIRouter(prefix="/restrictions", tags=["restrictions"])


@router.get("/", response_model=list[RestriccionRead], summary="Listar restricciones")
def list_restrictions(
        hijo_id: int | None = None,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ✅ Listar restricciones alimentarias

    Privilegios:
    - Todos pueden consultar (pero solo las de sus hijos)
    """
    return crud.list_(db, hijo_id=hijo_id)


@router.get("/{restriccion_id}", response_model=RestriccionRead, summary="Obtener restricción")
def get_restriction(
        restriccion_id: int,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """✅ Obtener detalle de una restricción"""
    obj = crud.get(db, restriccion_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No existe")
    return obj


@router.post("/", response_model=RestriccionRead, status_code=status.HTTP_201_CREATED, summary="Crear restricción")
def create_restriction(
        payload: RestriccionCreate,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ⚠️ CONFIGURAR RESTRICCIONES ALIMENTARIAS

    Privilegios según membresía:
    - Premium: ✅ Puede crear restricciones
    - Estándar: ✅ Puede crear restricciones
    - Básico: ❌ NO puede

    Tipos de restricciones:
    1. ALERGIA: Asociada a un alimento específico (requiere alimento_id)
       Ejemplo: { tipo: "alergia", alimento_id: 5, hijo_id: 3 }

    2. PROHIBIDO: Match por texto en nombre del alimento (requiere texto)
       Ejemplo: { tipo: "prohibido", texto: "chocolate", hijo_id: 3 }
    """
    if not can_configure_restrictions(current_user):
        raise PermissionDenied(
            "Tu plan actual no permite configurar restricciones alimentarias. "
            "Actualiza a Estándar o Premium para usar esta funcionalidad."
        )

    try:
        return crud.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{restriccion_id}", response_model=RestriccionRead, summary="Actualizar restricción")
def update_restriction(
        restriccion_id: int,
        payload: RestriccionUpdate,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ⚠️ Actualizar restricción existente
    Requiere Estándar o Premium
    """
    if not can_configure_restrictions(current_user):
        raise PermissionDenied("Solo Estándar y Premium pueden modificar restricciones")

    try:
        return crud.update(db, restriccion_id, payload)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{restriccion_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar restricción")
def delete_restriction(
        restriccion_id: int,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ⚠️ Eliminar restricción
    Requiere Estándar o Premium
    """
    if not can_configure_restrictions(current_user):
        raise PermissionDenied("Solo Estándar y Premium pueden eliminar restricciones")

    try:
        crud.delete(db, restriccion_id)
        return
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))