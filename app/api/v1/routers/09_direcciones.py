from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.core.deps import get_db, get_current_user
from app.db.models.direccion import Direccion
from app.db.models.usuario import Usuario
from app.db.schemas.direccion import DireccionCreate, DireccionUpdate, DireccionRead

router = APIRouter(prefix="/direcciones", tags=["09 - Direcciones"])

@router.post("/", response_model=DireccionRead, status_code=status.HTTP_201_CREATED, summary="Crear dirección")
def create_direccion(
    payload: DireccionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear una nueva dirección (respetando límites de membresía)"""
    # Verificar que el usuario cree para sí mismo
    if payload.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes crear direcciones para otro usuario")
    
    # Verificar límite de direcciones según membresía
    limite = current_user.membresia.max_direcciones if current_user.membresia else 1
    count = db.scalar(func.count(Direccion.id).where(Direccion.usuario_id == current_user.id))
    
    if count >= limite:
        raise HTTPException(
            status_code=400, 
            detail=f"Has alcanzado el límite de {limite} direcciones para tu plan {current_user.membresia.tipo}"
        )
    
    direccion = Direccion(**payload.model_dump())
    db.add(direccion)
    db.commit()
    db.refresh(direccion)
    return direccion

@router.get("/me", response_model=List[DireccionRead], summary="Listar mis direcciones")
def list_my_direcciones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar las direcciones del usuario autenticado"""
    return db.query(Direccion).filter_by(usuario_id=current_user.id).all()

@router.get("/{direccion_id}", response_model=DireccionRead, summary="Ver dirección")
def get_direccion(
    direccion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener una dirección por ID"""
    direccion = db.get(Direccion, direccion_id)
    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    
    if direccion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta dirección")
    
    return direccion

@router.patch("/{direccion_id}", response_model=DireccionRead, summary="Actualizar dirección")
def update_direccion(
    direccion_id: int,
    payload: DireccionUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar una dirección"""
    direccion = db.get(Direccion, direccion_id)
    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    
    if direccion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes editar esta dirección")
    
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(direccion, key, value)
    
    db.commit()
    db.refresh(direccion)
    return direccion

@router.delete("/{direccion_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar dirección")
def delete_direccion(
    direccion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar una dirección"""
    direccion = db.get(Direccion, direccion_id)
    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    
    if direccion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes eliminar esta dirección")
    
    db.delete(direccion)
    db.commit()
    return None
