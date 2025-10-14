from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.db.schemas.restriction import RestriccionCreate, RestriccionRead, RestriccionUpdate
from app.crud import restriction as crud

router = APIRouter(prefix="/restrictions", tags=["restrictions"])

@router.get("/", response_model=list[RestriccionRead])
def list_restrictions(hijo_id: int | None = None, db: Session = Depends(get_db)):
    return crud.list_(db, hijo_id=hijo_id)

@router.get("/{restriccion_id}", response_model=RestriccionRead)
def get_restriction(restriccion_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, restriccion_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No existe")
    return obj

@router.post("/", response_model=RestriccionRead, status_code=status.HTTP_201_CREATED)
def create_restriction(payload: RestriccionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{restriccion_id}", response_model=RestriccionRead)
def update_restriction(restriccion_id: int, payload: RestriccionUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update(db, restriccion_id, payload)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{restriccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restriction(restriccion_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete(db, restriccion_id)
        return
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
