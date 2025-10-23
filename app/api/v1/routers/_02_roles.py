from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.core_models import Rol
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/roles", tags=["02 - Roles"])

class RolCreate(BaseModel):
    nombre: str

class RolRead(BaseModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True

@router.get("/", response_model=list[RolRead])
def listar_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()

@router.post("/", response_model=RolRead, status_code=201)
def crear_rol(payload: RolCreate, db: Session = Depends(get_db)):
    rol = Rol(nombre=payload.nombre)
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol
