from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.db.models.alimento import Alimento
from app.db.schemas.alimento import AlimentoCreate, AlimentoUpdate, AlimentoRead

router = APIRouter(prefix="/alimentos", tags=["06 - Alimentos"])

@router.post("/", response_model=AlimentoRead, status_code=status.HTTP_201_CREATED, summary="Crear alimento (Admin)")
def create_alimento(payload: AlimentoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo alimento en el catálogo (solo Admin)"""
    # Verificar que no exista
    if db.query(Alimento).filter_by(nombre=payload.nombre).first():
        raise HTTPException(status_code=400, detail="Ya existe un alimento con ese nombre")
    
    alimento = Alimento(**payload.model_dump())
    db.add(alimento)
    db.commit()
    db.refresh(alimento)
    return alimento

@router.get("/", response_model=List[AlimentoRead], summary="Listar alimentos activos")
def list_alimentos(
    activos_solo: bool = True,
    db: Session = Depends(get_db)
):
    """Listar todos los alimentos (solo activos por defecto)"""
    query = db.query(Alimento)
    if activos_solo:
        query = query.filter_by(activo=True)
    return query.all()

@router.get("/{alimento_id}", response_model=AlimentoRead, summary="Ver alimento")
def get_alimento(alimento_id: int, db: Session = Depends(get_db)):
    """Obtener un alimento por ID"""
    alimento = db.get(Alimento, alimento_id)
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return alimento

@router.patch("/{alimento_id}", response_model=AlimentoRead, summary="Actualizar alimento (Admin)")
def update_alimento(
    alimento_id: int,
    payload: AlimentoUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un alimento (solo Admin)"""
    alimento = db.get(Alimento, alimento_id)
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(alimento, key, value)
    
    db.commit()
    db.refresh(alimento)
    return alimento

@router.delete("/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Desactivar alimento (Admin)")
def delete_alimento(alimento_id: int, db: Session = Depends(get_db)):
    """Desactivar un alimento (soft delete) - solo Admin"""
    alimento = db.get(Alimento, alimento_id)
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    
    # Soft delete
    alimento.activo = False
    db.commit()
    return None
