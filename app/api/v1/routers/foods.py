from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security_deps import get_current_admin_user
from app.db.schemas.food import AlimentoCreate, AlimentoUpdate, AlimentoRead
from app.crud import alimento as crud

router = APIRouter(prefix="/foods", tags=["foods"])

@router.get("/", response_model=list[AlimentoRead], summary="Listar alimentos")
def list_foods(
    only_active: str = Query("true", description="true=activos, false=inactivos, all=todos"),
    db: Session = Depends(get_db)
):
    """
    Filtros: (LECTURA PERMITIDA A TODOS)
    """
    return crud.list_(db, only_active=only_active)

@router.get("/{food_id}", response_model=AlimentoRead, summary="Obtener un alimento")
def get_food(food_id: int, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    return obj

@router.post("/", response_model=AlimentoRead, status_code=status.HTTP_201_CREATED, summary="Crear alimento (Admin)")
def create_food(
    payload: AlimentoCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user) # <-- Seguridad Admin
):
    if crud.exists_by_name(db, payload.nombre):
        raise HTTPException(status_code=400, detail="El alimento ya existe")
    return crud.create(db, payload)

@router.patch("/{food_id}", response_model=AlimentoRead, summary="Actualizar alimento (Admin)")
def update_food(
    food_id: int, 
    payload: AlimentoUpdate, 
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user) # <-- Seguridad Admin
):
    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    return crud.update(db, obj, payload)

@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Desactivar alimento (Admin)")
def delete_food(
    food_id: int, 
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user) # <-- Seguridad Admin
):
    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    crud.soft_delete(db, obj)
    return
