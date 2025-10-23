from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.deps import get_db, get_current_user
from app.db.models.lonchera import Lonchera
from app.db.models.hijo import Hijo
from app.db.models.usuario import Usuario
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/loncheras", tags=["07 - Loncheras"])

# Schemas
class LoncheraCreate(BaseModel):
    hijo_id: int
    fecha: date
    direccion_id: int | None = None

class LoncheraUpdate(BaseModel):
    fecha: date | None = None
    estado: str | None = None
    direccion_id: int | None = None

class LoncheraRead(BaseModel):
    id: int
    hijo_id: int
    fecha: date
    estado: str
    direccion_id: int | None
    model_config = ConfigDict(from_attributes=True)

@router.post("/", response_model=LoncheraRead, status_code=status.HTTP_201_CREATED, summary="Crear lonchera")
def create_lonchera(
    payload: LoncheraCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear una nueva lonchera para un hijo"""
    # Verificar que el hijo exista y pertenezca al usuario
    hijo = db.get(Hijo, payload.hijo_id)
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    if hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes crear loncheras para hijos de otro usuario")
    
    lonchera = Lonchera(**payload.model_dump())
    db.add(lonchera)
    db.commit()
    db.refresh(lonchera)
    return lonchera

@router.get("/", response_model=List[LoncheraRead], summary="Listar loncheras")
def list_loncheras(
    hijo_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar loncheras del usuario autenticado (filtrable por hijo)"""
    query = db.query(Lonchera).join(Hijo).filter(Hijo.usuario_id == current_user.id)
    
    if hijo_id:
        query = query.filter(Lonchera.hijo_id == hijo_id)
    
    return query.all()

@router.get("/{lonchera_id}", response_model=LoncheraRead, summary="Ver lonchera")
def get_lonchera(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener una lonchera por ID"""
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    
    # Verificar que pertenezca al usuario
    if lonchera.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta lonchera")
    
    return lonchera

@router.patch("/{lonchera_id}", response_model=LoncheraRead, summary="Actualizar lonchera")
def update_lonchera(
    lonchera_id: int,
    payload: LoncheraUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar una lonchera"""
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    
    if lonchera.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes editar esta lonchera")
    
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(lonchera, key, value)
    
    db.commit()
    db.refresh(lonchera)
    return lonchera

@router.delete("/{lonchera_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar lonchera")
def delete_lonchera(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar una lonchera"""
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    
    if lonchera.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes eliminar esta lonchera")
    
    db.delete(lonchera)
    db.commit()
    return None
