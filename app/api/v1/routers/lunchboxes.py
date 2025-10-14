from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.db.schemas.lunchbox import (
    LoncheraCreate, LoncheraRead, LoncheraUpdate,
    LoncheraItemCreate, LoncheraItemUpdate,
    LoncheraItemRead, LoncheraDetailRead
)
from app.crud import lunchbox as crud

router = APIRouter(prefix="/lunchboxes", tags=["lunchboxes"])

@router.get("/", response_model=list[LoncheraRead])
def list_lunchboxes(hijo_id: int | None = None, db: Session = Depends(get_db)):
    return crud.list_(db, hijo_id=hijo_id)

@router.get("/{lunchbox_id}", response_model=LoncheraRead)
def get_lunchbox(lunchbox_id: int, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, lunchbox_id)
    if not obj: raise HTTPException(status_code=404, detail="No encontrado")
    return obj

@router.get("/{lunchbox_id}/items", response_model=list[LoncheraItemRead])
def list_lunchbox_items(lunchbox_id: int, db: Session = Depends(get_db)):
    return crud.list_items(db, lunchbox_id)

@router.get("/{lunchbox_id}/detail", response_model=LoncheraDetailRead)
def get_lunchbox_detail(lunchbox_id: int, db: Session = Depends(get_db)):
    data = crud.get_detail(db, lunchbox_id)
    if not data: raise HTTPException(status_code=404, detail="No encontrado")
    return data

@router.post("/", response_model=LoncheraRead, status_code=status.HTTP_201_CREATED)
def create_lunchbox(payload: LoncheraCreate, db: Session = Depends(get_db)):
    try:
        return crud.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{lunchbox_id}", response_model=LoncheraRead)
def update_lunchbox(lunchbox_id: int, payload: LoncheraUpdate, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, lunchbox_id)
    if not obj: raise HTTPException(status_code=404, detail="No encontrado")
    try:
        return crud.update(db, obj, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{lunchbox_id}/items", status_code=status.HTTP_201_CREATED)
def add_item(lunchbox_id: int, item: LoncheraItemCreate, db: Session = Depends(get_db)):
    try:
        crud.add_item(db, lunchbox_id, item); return {"ok": True}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{lunchbox_id}/items/{alimento_id}", status_code=status.HTTP_200_OK)
def update_item(lunchbox_id: int, alimento_id: int, payload: LoncheraItemUpdate, db: Session = Depends(get_db)):
    try:
        crud.update_item(db, lunchbox_id, alimento_id, payload); return {"ok": True}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{lunchbox_id}/items/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(lunchbox_id: int, alimento_id: int, db: Session = Depends(get_db)):
    try:
        crud.remove_item(db, lunchbox_id, alimento_id); return
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
