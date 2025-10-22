from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.schemas.restriccion import RestriccionCreate, RestriccionUpdate, RestriccionRead
from app.db.models.restriccion import Restriccion
from app.db.models.core_models import Hijo
from app.core.deps import get_current_user

router = APIRouter(prefix="/restricciones", tags=["restricciones"])

@router.get("/", response_model=List[RestriccionRead])
def listar_restricciones(
    hijo_id: int | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Listar restricciones (filtrar por hijo si se especifica)"""
    query = db.query(Restriccion).join(Hijo).filter(Hijo.usuario_id == current_user.id)
    
    if hijo_id:
        query = query.filter(Restriccion.hijo_id == hijo_id)
    
    return query.all()

@router.get("/{restriccion_id}", response_model=RestriccionRead)
def obtener_restriccion(
    restriccion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener una restricción por ID"""
    restriccion = db.query(Restriccion).join(Hijo).filter(
        Restriccion.id == restriccion_id,
        Hijo.usuario_id == current_user.id
    ).first()
    
    if not restriccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restricción no encontrada"
        )
    return restriccion

@router.post("/", response_model=RestriccionRead, status_code=status.HTTP_201_CREATED)
def crear_restriccion(
    restriccion: RestriccionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear una nueva restricción"""
    # Verificar que el hijo pertenece al usuario
    hijo = db.query(Hijo).filter(
        Hijo.id == restriccion.hijo_id,
        Hijo.usuario_id == current_user.id
    ).first()
    
    if not hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    # Validar según tipo
    if restriccion.tipo == "alergia" and not restriccion.alimento_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las alergias requieren especificar un alimento_id"
        )
    
    if restriccion.tipo == "prohibido" and not restriccion.texto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las restricciones prohibidas requieren especificar texto"
        )
    
    db_restriccion = Restriccion(**restriccion.model_dump())
    db.add(db_restriccion)
    db.commit()
    db.refresh(db_restriccion)
    return db_restriccion

@router.patch("/{restriccion_id}", response_model=RestriccionRead)
def actualizar_restriccion(
    restriccion_id: int,
    restriccion: RestriccionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar una restricción"""
    db_restriccion = db.query(Restriccion).join(Hijo).filter(
        Restriccion.id == restriccion_id,
        Hijo.usuario_id == current_user.id
    ).first()
    
    if not db_restriccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restricción no encontrada"
        )
    
    update_data = restriccion.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_restriccion, key, value)
    
    db.commit()
    db.refresh(db_restriccion)
    return db_restriccion

@router.delete("/{restriccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_restriccion(
    restriccion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Eliminar una restricción"""
    db_restriccion = db.query(Restriccion).join(Hijo).filter(
        Restriccion.id == restriccion_id,
        Hijo.usuario_id == current_user.id
    ).first()
    
    if not db_restriccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restricción no encontrada"
        )
    
    db.delete(db_restriccion)
    db.commit()
    return None
