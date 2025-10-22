from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.db.session import get_db
from app.db.schemas.direccion import DireccionCreate, DireccionUpdate, DireccionRead
from app.db.models.direccion import Direccion
from app.core.deps import get_current_user

router = APIRouter(prefix="/direcciones", tags=["direcciones"])

@router.get("/", response_model=List[DireccionRead])
def listar_direcciones(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Listar todas las direcciones del usuario actual"""
    return db.query(Direccion).filter(Direccion.usuario_id == current_user.id).all()

@router.get("/{direccion_id}", response_model=DireccionRead)
def obtener_direccion(
    direccion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener una dirección por ID"""
    direccion = db.query(Direccion).filter(
        Direccion.id == direccion_id,
        Direccion.usuario_id == current_user.id
    ).first()
    
    if not direccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dirección no encontrada"
        )
    return direccion

@router.post("/", response_model=DireccionRead, status_code=status.HTTP_201_CREATED)
def crear_direccion(
    direccion: DireccionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear una nueva dirección"""
    # Verificar límite según membresía
    limite = current_user.membresia.max_direcciones
    count = db.query(func.count()).select_from(Direccion).filter(
        Direccion.usuario_id == current_user.id
    ).scalar()
    
    if limite > 0 and count >= limite:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Límite de direcciones alcanzado ({limite}). Actualiza tu membresía."
        )
    
    db_direccion = Direccion(
        usuario_id=current_user.id,
        etiqueta=direccion.etiqueta,
        direccion=direccion.direccion,
        barrio=direccion.barrio,
        ciudad=direccion.ciudad
    )
    db.add(db_direccion)
    db.commit()
    db.refresh(db_direccion)
    return db_direccion

@router.patch("/{direccion_id}", response_model=DireccionRead)
def actualizar_direccion(
    direccion_id: int,
    direccion: DireccionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar una dirección"""
    db_direccion = db.query(Direccion).filter(
        Direccion.id == direccion_id,
        Direccion.usuario_id == current_user.id
    ).first()
    
    if not db_direccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dirección no encontrada"
        )
    
    update_data = direccion.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_direccion, key, value)
    
    db.commit()
    db.refresh(db_direccion)
    return db_direccion

@router.delete("/{direccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_direccion(
    direccion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Eliminar una dirección"""
    db_direccion = db.query(Direccion).filter(
        Direccion.id == direccion_id,
        Direccion.usuario_id == current_user.id
    ).first()
    
    if not db_direccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dirección no encontrada"
        )
    
    db.delete(db_direccion)
    db.commit()
    return None
