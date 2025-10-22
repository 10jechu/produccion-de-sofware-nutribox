from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.models import Usuario

router = APIRouter(prefix="/api/v1/usuarios", tags=["usuarios"])

@router.post("/", response_model=Usuario)
def crear_usuario(data: Usuario, db: Session = Depends(get_session)):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
