from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.db.models.hijo import Hijo
from app.db.models.usuario import Usuario
from app.db.schemas.hijo import HijoCreate, HijoUpdate, HijoRead

router = APIRouter(prefix="/hijos", tags=["05 - Hijos"])

@router.post("/", response_model=HijoRead, status_code=status.HTTP_201_CREATED, summary="Crear hijo")
def create_hijo(
    payload: HijoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear un nuevo hijo (Usuario Principal)"""
    # Verificar que el hijo sea del usuario autenticado
    if payload.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes crear hijos para otro usuario")
    
    hijo = Hijo(**payload.model_dump())
    db.add(hijo)
    db.commit()
    db.refresh(hijo)
    return hijo

@router.get("/me", response_model=List[HijoRead], summary="Listar mis hijos")
def list_my_hijos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar los hijos del usuario autenticado"""
    return db.query(Hijo).filter_by(usuario_id=current_user.id).all()

@router.get("/{hijo_id}", response_model=HijoRead, summary="Ver hijo")
def get_hijo(hijo_id: int, db: Session = Depends(get_db)):
    """Obtener un hijo por ID"""
    hijo = db.get(Hijo, hijo_id)
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    return hijo

@router.patch("/{hijo_id}", response_model=HijoRead, summary="Actualizar hijo")
def update_hijo(
    hijo_id: int,
    payload: HijoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar información de un hijo"""
    hijo = db.get(Hijo, hijo_id)
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    # Verificar que el hijo pertenezca al usuario
    if hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes editar hijos de otro usuario")
    
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(hijo, key, value)
    
    db.commit()
    db.refresh(hijo)
    return hijo

@router.delete("/{hijo_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar hijo")
def delete_hijo(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar un hijo"""
    hijo = db.get(Hijo, hijo_id)
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    if hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes eliminar hijos de otro usuario")
    
    db.delete(hijo)
    db.commit()
    return None
