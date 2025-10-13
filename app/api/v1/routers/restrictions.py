from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.db.schemas.restriction import RestriccionCreate, RestriccionRead
from app.crud import restriction as crud

router = APIRouter()

@router.get("/", response_model=list[RestriccionRead])
def list_restrictions(hijo_id: int | None = None, db: Session = Depends(get_db)):
    return crud.list_(db, hijo_id=hijo_id)

@router.post("/", response_model=RestriccionRead, status_code=status.HTTP_201_CREATED)
def create_restriction(payload: RestriccionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{restriccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restriction(restriccion_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete(db, restriccion_id)
        return
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
