from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.restriccion import Restriccion
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1/restricciones", tags=["09 - Restricciones"])

class RestriccionCreate(BaseModel):
    hijo_id: int
    tipo: str
    alimento_id: Optional[int] = None
    texto: Optional[str] = None

class RestriccionRead(BaseModel):
    id: int
    hijo_id: int
    tipo: str
    alimento_id: Optional[int]
    texto: Optional[str]
    class Config:
        from_attributes = True

@router.post("/", response_model=RestriccionRead, status_code=201)
def crear_restriccion(payload: RestriccionCreate, db: Session = Depends(get_db)):
    obj = Restriccion(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[RestriccionRead])
def listar_restricciones(db: Session = Depends(get_db)):
    return db.query(Restriccion).all()

@router.delete("/{id}", status_code=204)
def eliminar_restriccion(id: int, db: Session = Depends(get_db)):
    obj = db.get(Restriccion, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Restricción no encontrada")
    db.delete(obj)
    db.commit()
