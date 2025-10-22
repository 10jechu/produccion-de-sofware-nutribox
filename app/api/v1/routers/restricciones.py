from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from app.db.session import get_session
from app.models import Restriccion

router = APIRouter(prefix="/api/v1/restriccions", tags=["restricciones"])

@router.get("/", response_model=List[Restriccion])
def listar(db: Session = Depends(get_session)):
    return db.exec(select(Restriccion)).all()

@router.post("/", response_model=Restriccion)
def crear(data: Restriccion, db: Session = Depends(get_session)):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
