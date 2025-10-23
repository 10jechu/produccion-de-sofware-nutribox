from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.db.models.usuario import Usuario
from pydantic import BaseModel, EmailStr, ConfigDict

router = APIRouter(prefix="/usuarios", tags=["02 - Usuarios"])

# Schemas
class UsuarioRead(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    estado: str
    activo: bool
    model_config = ConfigDict(from_attributes=True)

class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    estado: str | None = None
    activo: bool | None = None

# Endpoints
@router.get("/me", response_model=UsuarioRead, summary="Ver mi perfil")
def get_my_profile(current_user: Usuario = Depends(get_current_user)):
    """Obtener información del usuario autenticado"""
    return current_user

@router.put("/me", response_model=UsuarioRead, summary="Actualizar mi perfil")
def update_my_profile(
    payload: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar información del usuario autenticado"""
    if payload.nombre:
        current_user.nombre = payload.nombre
    if payload.estado:
        current_user.estado = payload.estado
    if payload.activo is not None:
        current_user.activo = payload.activo
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/", response_model=List[UsuarioRead], summary="Listar usuarios (Admin)")
def list_users(db: Session = Depends(get_db)):
    """Listar todos los usuarios (solo Admin)"""
    return db.query(Usuario).all()

@router.get("/{user_id}", response_model=UsuarioRead, summary="Ver usuario (Admin)")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID (solo Admin)"""
    user = db.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
