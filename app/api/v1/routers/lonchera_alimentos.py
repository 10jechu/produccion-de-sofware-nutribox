from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from app.db.session import get_session
from app.models import LoncheraAlimento

router = APIRouter(prefix="/api/v1/lonchera_alimentos", tags=["lonchera_alimentos"])

@router.get("/", response_model=List[LoncheraAlimento])
def listar(db: Session = Depends(get_session)):
    return db.exec(select(LoncheraAlimento)).all()

@router.post("/", response_model=LoncheraAlimento)
def crear(data: LoncheraAlimento, db: Session = Depends(get_session)):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.delete("/{lonchera_id}/{alimento_id}")
def borrar(lonchera_id: int, alimento_id: int, db: Session = Depends(get_session)):
    obj = db.get(LoncheraAlimento, (lonchera_id, alimento_id))
    if not obj:
        raise HTTPException(404, "Relación no encontrada")
    db.delete(obj)
    db.commit()
    return {"ok": True}
