from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.db.schemas.lunchbox import LoncheraCreate, LoncheraRead, LoncheraItemCreate
from app.crud import lunchbox as crud

router = APIRouter()

@router.get("/", response_model=list[LoncheraRead])
def list_lunchboxes(hijo_id: int | None = None, db: Session = Depends(get_db)):
    return crud.list_(db, hijo_id=hijo_id)

@router.post("/", response_model=LoncheraRead, status_code=status.HTTP_201_CREATED)
def create_lunchbox(payload: LoncheraCreate, db: Session = Depends(get_db)):
    try:
        return crud.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{lunchbox_id}/items", status_code=status.HTTP_201_CREATED)
def add_item(lunchbox_id: int, item: LoncheraItemCreate, db: Session = Depends(get_db)):
    try:
        crud.add_item(db, lunchbox_id, item)
        return {"ok": True}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{lunchbox_id}/items/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(lunchbox_id: int, alimento_id: int, db: Session = Depends(get_db)):
    try:
        crud.remove_item(db, lunchbox_id, alimento_id)
        return
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
