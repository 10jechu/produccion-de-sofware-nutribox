from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.core.permissions import can_manage_foods, PermissionDenied
from app.db.schemas.food import AlimentoCreate, AlimentoUpdate, AlimentoRead
from app.db.models.core_models import Usuario
from app.crud import alimento as crud

router = APIRouter(prefix="/foods", tags=["foods"])


@router.get("/", response_model=list[AlimentoRead], summary="Listar alimentos")
def list_foods(
        only_active: str = Query("true", description="true=activos, false=inactivos, all=todos"),
        db: Session = Depends(get_db)
):
    """
    Filtros:
    - true: Solo alimentos activos
    - false: Solo alimentos inactivos (eliminados)
    - all: Todos los alimentos

    ✅ TODOS los usuarios pueden ver el catálogo de alimentos
    """
    return crud.list_(db, only_active=only_active)


@router.get("/{food_id}", response_model=AlimentoRead, summary="Obtener un alimento")
def get_food(food_id: int, db: Session = Depends(get_db)):
    """✅ TODOS pueden ver detalles de un alimento"""
    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    return obj


@router.post("/", response_model=AlimentoRead, status_code=status.HTTP_201_CREATED, summary="Crear alimento")
def create_food(
        payload: AlimentoCreate,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ⚠️ SOLO Admin o Premium pueden crear alimentos

    Privilegios según membresía:
    - Admin: Siempre puede
    - Premium: Puede agregar al catálogo
    - Estándar/Free: NO pueden
    """
    if not can_manage_foods(current_user):
        raise PermissionDenied(
            "Solo usuarios Premium o Administradores pueden crear alimentos. "
            f"Tu plan actual: {current_user.membresia.tipo if current_user.membresia else 'Ninguno'}"
        )

    if crud.exists_by_name(db, payload.nombre):
        raise HTTPException(status_code=400, detail="El alimento ya existe")

    return crud.create(db, payload)


@router.patch("/{food_id}", response_model=AlimentoRead, summary="Actualizar alimento")
def update_food(
        food_id: int,
        payload: AlimentoUpdate,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ⚠️ SOLO Admin o Premium pueden actualizar alimentos
    """
    if not can_manage_foods(current_user):
        raise PermissionDenied(
            "Solo usuarios Premium o Administradores pueden editar alimentos"
        )

    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")

    return crud.update(db, obj, payload)


@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Desactivar alimento")
def delete_food(
        food_id: int,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    """
    ⚠️ SOLO Admin o Premium pueden desactivar alimentos (soft delete)
    """
    if not can_manage_foods(current_user):
        raise PermissionDenied(
            "Solo usuarios Premium o Administradores pueden eliminar alimentos"
        )

    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")

    crud.soft_delete(db, obj)
    return