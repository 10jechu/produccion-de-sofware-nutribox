from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from app.db.session import get_session
from app.models import Hijo

router = APIRouter(prefix="/api/v1/hijos", tags=["hijos"])

@router.get("/", response_model=List[Hijo])
def listar(db: Session = Depends(get_session)):
    return db.exec(select(Hijo)).all()

@router.post("/", response_model=Hijo)
def crear(data: Hijo, db: Session = Depends(get_session)):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.patch("/{hijo_id}", response_model=Hijo)
def actualizar(hijo_id: int, parcial: dict, db: Session = Depends(get_session)):
    hijo = db.get(Hijo, hijo_id)
    if not hijo:
        raise HTTPException(404, "Hijo no encontrado")
    for k, v in parcial.items():
        setattr(hijo, k, v)
    db.add(hijo)
    db.commit()
    db.refresh(hijo)
    return hijo

@router.delete("/{hijo_id}")
def borrar(hijo_id: int, db: Session = Depends(get_session)):
    hijo = db.get(Hijo, hijo_id)
    if not hijo:
        raise HTTPException(404, "Hijo no encontrado")
    db.delete(hijo)
    db.commit()
    return {"ok": True}
