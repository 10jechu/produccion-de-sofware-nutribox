# app/api/v1/routers/foods.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
# Asegúrate de importar get_db Y la nueva dependencia require_admin
from app.core.deps import get_db, require_admin
from app.db.schemas.food import AlimentoCreate, AlimentoUpdate, AlimentoRead
from app.crud import alimento as crud
# Importa Usuario si necesitas la anotación de tipo para el usuario admin
from app.db.models.core_models import Usuario

router = APIRouter(prefix="/foods", tags=["foods"])

# GET /foods (Listar) - Puede ser público o solo para usuarios logueados (Depends(get_db) o Depends(get_current_user))
@router.get("/", response_model=list[AlimentoRead], summary="Listar alimentos")
def list_foods(
    only_active: str = Query("true", description="true=activos, false=inactivos, all=todos"),
    db: Session = Depends(get_db) # Abierto a todos por ahora
):
    # ... (lógica existente) ...
    return crud.list_(db, only_active=only_active)

# GET /foods/{id} (Obtener uno) - Puede ser público o solo para usuarios logueados
@router.get("/{food_id}", response_model=AlimentoRead, summary="Obtener un alimento")
def get_food(food_id: int, db: Session = Depends(get_db)): # Abierto a todos
    # ... (lógica existente) ...
    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    return obj

# --- Endpoints protegidos solo para Admin ---

# POST /foods (Crear) - SOLO ADMIN
@router.post("/", response_model=AlimentoRead, status_code=status.HTTP_201_CREATED, summary="Crear alimento (Admin Only)")
def create_food(
    payload: AlimentoCreate,
    db: Session = Depends(get_db),
    admin_user: Usuario = Depends(require_admin) # <-- APLICA LA DEPENDENCIA ADMIN
):
    if crud.exists_by_name(db, payload.nombre):
        raise HTTPException(status_code=400, detail="El alimento ya existe")
    return crud.create(db, payload)

# PATCH /foods/{id} (Actualizar) - SOLO ADMIN
@router.patch("/{food_id}", response_model=AlimentoRead, summary="Actualizar alimento (Admin Only)")
def update_food(
    food_id: int,
    payload: AlimentoUpdate,
    db: Session = Depends(get_db),
    admin_user: Usuario = Depends(require_admin) # <-- APLICA LA DEPENDENCIA ADMIN
):
    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    return crud.update(db, obj, payload)

# DELETE /foods/{id} (Desactivar/Soft Delete) - SOLO ADMIN
@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Desactivar alimento (Admin Only)")
def delete_food(
    food_id: int,
    db: Session = Depends(get_db),
    admin_user: Usuario = Depends(require_admin) # <-- APLICA LA DEPENDENCIA ADMIN
):
    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    crud.soft_delete(db, obj) # El CRUD ya hace soft delete
    return