from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.db.schemas.address import DireccionCreate, DireccionRead
from app.crud import address as crud

router = APIRouter()

@router.get("/", response_model=list[DireccionRead])
def list_addresses(usuario_id: int, db: Session = Depends(get_db)):
    return crud.list_by_user(db, usuario_id)

@router.post("/", response_model=DireccionRead, status_code=status.HTTP_201_CREATED)
def create_address(payload: DireccionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=400, detail=str(e))
