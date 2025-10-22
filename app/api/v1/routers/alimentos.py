from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.schemas.alimento import AlimentoCreate, AlimentoUpdate, AlimentoRead
from app.crud import crud_alimento
from app.core.deps import get_current_user

router = APIRouter(prefix="/alimentos", tags=["alimentos"])

@router.get("/", response_model=List[AlimentoRead])
def listar_alimentos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar todos los alimentos activos"""
    return crud_alimento.get_all(db, skip=skip, limit=limit)

@router.get("/{alimento_id}", response_model=AlimentoRead)
def obtener_alimento(alimento_id: int, db: Session = Depends(get_db)):
    """Obtener un alimento por ID"""
    alimento = crud_alimento.get_by_id(db, alimento_id)
    if not alimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alimento no encontrado"
        )
    return alimento

@router.post("/", response_model=AlimentoRead, status_code=status.HTTP_201_CREATED)
def crear_alimento(
    alimento: AlimentoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear un nuevo alimento (solo administradores)"""
    # Verificar que sea administrador
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden crear alimentos"
        )
    
    return crud_alimento.create(db, alimento)

@router.patch("/{alimento_id}", response_model=AlimentoRead)
def actualizar_alimento(
    alimento_id: int,
    alimento: AlimentoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar un alimento (solo administradores)"""
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden actualizar alimentos"
        )
    
    updated = crud_alimento.update(db, alimento_id, alimento)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alimento no encontrado"
        )
    return updated

@router.delete("/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_alimento(
    alimento_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Eliminar un alimento (soft delete, solo administradores)"""
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden eliminar alimentos"
        )
    
    deleted = crud_alimento.delete(db, alimento_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alimento no encontrado"
        )
    return None
