from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.core_models import Membresia
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/membresias", tags=["03 - Membresías"])

class MembresiaCreate(BaseModel):
    tipo: str
    max_direcciones: int = 0

class MembresiaRead(BaseModel):
    id: int
    tipo: str
    max_direcciones: int
    class Config:
        from_attributes = True

@router.get("/", response_model=list[MembresiaRead])
def listar_membresias(db: Session = Depends(get_db)):
    return db.query(Membresia).all()

@router.post("/", response_model=MembresiaRead, status_code=201)
def crear_membresia(payload: MembresiaCreate, db: Session = Depends(get_db)):
    mem = Membresia(**payload.dict())
    db.add(mem)
    db.commit()
    db.refresh(mem)
    return mem
