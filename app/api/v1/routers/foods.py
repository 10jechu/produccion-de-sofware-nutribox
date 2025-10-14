from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.db.schemas.food import AlimentoCreate, AlimentoUpdate, AlimentoRead
from app.crud import alimento as crud

router = APIRouter(prefix="/foods", tags=["foods"])

@router.get("/", response_model=list[AlimentoRead])
def list_foods(only_active: bool = True, db: Session = Depends(get_db)):
    return crud.list_(db, only_active=only_active)

@router.get("/{food_id}", response_model=AlimentoRead)
def get_food(food_id: int, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    return obj

@router.post("/", response_model=AlimentoRead, status_code=status.HTTP_201_CREATED)
def create_food(payload: AlimentoCreate, db: Session = Depends(get_db)):
    if crud.exists_by_name(db, payload.nombre):
        raise HTTPException(status_code=400, detail="El alimento ya existe")
    return crud.create(db, payload)

@router.patch("/{food_id}", response_model=AlimentoRead)
def update_food(food_id: int, payload: AlimentoUpdate, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    return crud.update(db, obj, payload)

@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_food(food_id: int, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, food_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrado")
    crud.soft_delete(db, obj)
    return
