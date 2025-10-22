from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.schemas.lonchera import (
    LoncheraCreate, LoncheraUpdate, LoncheraRead,
    LoncheraItemCreate, LoncheraItemRead
)
from app.crud import crud_lonchera
from app.core.deps import get_current_user

router = APIRouter(prefix="/loncheras", tags=["loncheras"])

@router.get("/", response_model=List[LoncheraRead])
def listar_loncheras(
    hijo_id: int | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Listar loncheras (filtrar por hijo si se especifica)"""
    return crud_lonchera.get_all(db, hijo_id=hijo_id)

@router.get("/{lonchera_id}", response_model=LoncheraRead)
def obtener_lonchera(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener una lonchera por ID"""
    lonchera = crud_lonchera.get_by_id(db, lonchera_id)
    if not lonchera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lonchera no encontrada"
        )
    return lonchera

@router.post("/", response_model=LoncheraRead, status_code=status.HTTP_201_CREATED)
def crear_lonchera(
    lonchera: LoncheraCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear una nueva lonchera"""
    return crud_lonchera.create(db, lonchera)

@router.patch("/{lonchera_id}", response_model=LoncheraRead)
def actualizar_lonchera(
    lonchera_id: int,
    lonchera: LoncheraUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar una lonchera"""
    updated = crud_lonchera.update(db, lonchera_id, lonchera)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lonchera no encontrada"
        )
    return updated

@router.delete("/{lonchera_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_lonchera(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Eliminar una lonchera"""
    deleted = crud_lonchera.delete(db, lonchera_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lonchera no encontrada"
        )
    return None

# --- Items de lonchera ---

@router.post("/{lonchera_id}/items", status_code=status.HTTP_201_CREATED)
def agregar_item(
    lonchera_id: int,
    item: LoncheraItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Agregar un alimento a la lonchera"""
    # Verificar que la lonchera existe
    if not crud_lonchera.get_by_id(db, lonchera_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lonchera no encontrada"
        )
    
    crud_lonchera.add_item(db, lonchera_id, item)
    return {"message": "Item agregado exitosamente"}

@router.delete("/{lonchera_id}/items/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_item(
    lonchera_id: int,
    alimento_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Eliminar un alimento de la lonchera"""
    deleted = crud_lonchera.remove_item(db, lonchera_id, alimento_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    return None

@router.get("/{lonchera_id}/items", response_model=List[LoncheraItemRead])
def listar_items(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Listar todos los items de una lonchera"""
    items = crud_lonchera.get_items(db, lonchera_id)
    return [
        LoncheraItemRead(
            alimento_id=item.alimento_id,
            nombre=item.alimento.nombre,
            cantidad=item.cantidad
        )
        for item in items
    ]
