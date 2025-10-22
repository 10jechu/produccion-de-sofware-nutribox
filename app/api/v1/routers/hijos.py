from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.schemas.hijo import HijoCreate, HijoUpdate, HijoRead
from app.db.models.core_models import Hijo
from app.core.deps import get_current_user

router = APIRouter(prefix="/hijos", tags=["hijos"])

@router.get("/", response_model=List[HijoRead])
def listar_hijos(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Listar todos los hijos del usuario actual"""
    return db.query(Hijo).filter(Hijo.usuario_id == current_user.id).all()

@router.get("/{hijo_id}", response_model=HijoRead)
def obtener_hijo(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener un hijo por ID"""
    hijo = db.query(Hijo).filter(
        Hijo.id == hijo_id,
        Hijo.usuario_id == current_user.id
    ).first()
    
    if not hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    return hijo

@router.post("/", response_model=HijoRead, status_code=status.HTTP_201_CREATED)
def crear_hijo(
    hijo: HijoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear un nuevo hijo"""
    db_hijo = Hijo(
        nombre=hijo.nombre,
        fecha_nacimiento=str(hijo.fecha_nacimiento),
        usuario_id=current_user.id
    )
    db.add(db_hijo)
    db.commit()
    db.refresh(db_hijo)
    return db_hijo

@router.patch("/{hijo_id}", response_model=HijoRead)
def actualizar_hijo(
    hijo_id: int,
    hijo: HijoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar un hijo"""
    db_hijo = db.query(Hijo).filter(
        Hijo.id == hijo_id,
        Hijo.usuario_id == current_user.id
    ).first()
    
    if not db_hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    update_data = hijo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "fecha_nacimiento" and value:
            setattr(db_hijo, key, str(value))
        else:
            setattr(db_hijo, key, value)
    
    db.commit()
    db.refresh(db_hijo)
    return db_hijo

@router.delete("/{hijo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_hijo(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Eliminar un hijo"""
    db_hijo = db.query(Hijo).filter(
        Hijo.id == hijo_id,
        Hijo.usuario_id == current_user.id
    ).first()
    
    if not db_hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    db.delete(db_hijo)
    db.commit()
    return None
