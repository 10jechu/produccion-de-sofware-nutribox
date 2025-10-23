from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.db.models.membresia import Membresia
from app.db.models.usuario import Usuario
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/membresias", tags=["04 - Membresías"])

# Schemas
class MembresiaRead(BaseModel):
    id: int
    tipo: str
    max_direcciones: int
    precio: float | None
    descripcion: str | None
    model_config = ConfigDict(from_attributes=True)

# Endpoints
@router.get("/tipos", response_model=List[MembresiaRead], summary="Ver tipos de membresía")
def list_membership_types(db: Session = Depends(get_db)):
    """Listar todos los tipos de membresía disponibles"""
    return db.query(Membresia).all()

@router.get("/me", response_model=MembresiaRead, summary="Ver mi membresía actual")
def get_my_membership(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener la membresía del usuario autenticado"""
    if not current_user.membresia:
        raise HTTPException(status_code=404, detail="No tienes membresía asignada")
    return current_user.membresia

@router.post("/asignar/{user_id}/{membresia_id}", summary="Asignar membresía (Admin)")
def assign_membership(
    user_id: int,
    membresia_id: int,
    db: Session = Depends(get_db)
):
    """Asignar una membresía a un usuario (solo Admin)"""
    user = db.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    membresia = db.get(Membresia, membresia_id)
    if not membresia:
        raise HTTPException(status_code=404, detail="Membresía no encontrada")
    
    user.membresia_id = membresia_id
    db.commit()
    db.refresh(user)
    
    return {"message": f"Membresía '{membresia.tipo}' asignada a {user.nombre}"}
