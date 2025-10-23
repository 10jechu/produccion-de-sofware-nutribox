from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.direccion import Direccion
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/direcciones", tags=["08 - Direcciones"])

class DireccionCreate(BaseModel):
    usuario_id: int
    etiqueta: str = "Casa"
    direccion: str
    barrio: str = ""
    ciudad: str = "Bogotá"

class DireccionRead(BaseModel):
    id: int
    usuario_id: int
    etiqueta: str
    direccion: str
    barrio: str
    ciudad: str
    class Config:
        from_attributes = True

@router.post("/", response_model=DireccionRead, status_code=201)
def crear_direccion(payload: DireccionCreate, db: Session = Depends(get_db)):
    obj = Direccion(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[DireccionRead])
def listar_direcciones(db: Session = Depends(get_db)):
    return db.query(Direccion).all()

@router.delete("/{id}", status_code=204)
def eliminar_direccion(id: int, db: Session = Depends(get_db)):
    obj = db.get(Direccion, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    db.delete(obj)
    db.commit()
