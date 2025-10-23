from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.db.models.restriccion import Restriccion
from app.db.models.hijo import Hijo
from app.db.models.usuario import Usuario
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/restricciones", tags=["10 - Restricciones"])

# Schemas
class RestriccionCreate(BaseModel):
    hijo_id: int
    tipo: str  # 'alergia' o 'prohibido'
    alimento_id: int | None = None  # para tipo='alergia'
    texto: str | None = None  # para tipo='prohibido'

class RestriccionUpdate(BaseModel):
    tipo: str | None = None
    alimento_id: int | None = None
    texto: str | None = None

class RestriccionRead(BaseModel):
    id: int
    hijo_id: int
    tipo: str
    alimento_id: int | None
    texto: str | None
    model_config = ConfigDict(from_attributes=True)

@router.post("/", response_model=RestriccionRead, status_code=status.HTTP_201_CREATED, summary="Crear restricción")
def create_restriccion(
    payload: RestriccionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear una restricción alimentaria para un hijo"""
    # Verificar que el hijo exista y pertenezca al usuario
    hijo = db.get(Hijo, payload.hijo_id)
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    if hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes crear restricciones para hijos de otro usuario")
    
    # Validar según tipo
    if payload.tipo not in ["alergia", "prohibido"]:
        raise HTTPException(status_code=400, detail="Tipo debe ser 'alergia' o 'prohibido'")
    
    if payload.tipo == "alergia" and not payload.alimento_id:
        raise HTTPException(status_code=400, detail="Las alergias requieren alimento_id")
    
    if payload.tipo == "prohibido" and not payload.texto:
        raise HTTPException(status_code=400, detail="Las restricciones prohibidas requieren texto")
    
    restriccion = Restriccion(**payload.model_dump())
    db.add(restriccion)
    db.commit()
    db.refresh(restriccion)
    return restriccion

@router.get("/hijo/{hijo_id}", response_model=List[RestriccionRead], summary="Listar restricciones de un hijo")
def list_restricciones_by_hijo(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar todas las restricciones de un hijo"""
    hijo = db.get(Hijo, hijo_id)
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    if hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a este hijo")
    
    return db.query(Restriccion).filter_by(hijo_id=hijo_id).all()

@router.get("/{restriccion_id}", response_model=RestriccionRead, summary="Ver restricción")
def get_restriccion(
    restriccion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener una restricción por ID"""
    restriccion = db.get(Restriccion, restriccion_id)
    if not restriccion:
        raise HTTPException(status_code=404, detail="Restricción no encontrada")
    
    if restriccion.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta restricción")
    
    return restriccion

@router.patch("/{restriccion_id}", response_model=RestriccionRead, summary="Actualizar restricción")
def update_restriccion(
    restriccion_id: int,
    payload: RestriccionUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar una restricción"""
    restriccion = db.get(Restriccion, restriccion_id)
    if not restriccion:
        raise HTTPException(status_code=404, detail="Restricción no encontrada")
    
    if restriccion.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes editar esta restricción")
    
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(restriccion, key, value)
    
    db.commit()
    db.refresh(restriccion)
    return restriccion

@router.delete("/{restriccion_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar restricción")
def delete_restriccion(
    restriccion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar una restricción"""
    restriccion = db.get(Restriccion, restriccion_id)
    if not restriccion:
        raise HTTPException(status_code=404, detail="Restricción no encontrada")
    
    if restriccion.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes eliminar esta restricción")
    
    db.delete(restriccion)
    db.commit()
    return None
