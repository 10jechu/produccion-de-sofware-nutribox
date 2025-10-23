from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.core_models import Hijo, Usuario

def list_by_user(db: Session, usuario_id: int) -> list[Hijo]:
    """Lista todos los hijos de un usuario."""
    return db.scalars(select(Hijo).where(Hijo.usuario_id == usuario_id)).all()

def get_by_id(db: Session, child_id: int) -> Hijo | None:
    """Obtiene un hijo por ID."""
    return db.get(Hijo, child_id)

def create(db: Session, payload) -> Hijo:
    """Crea un nuevo hijo para un usuario."""
    user = db.get(Usuario, payload.usuario_id)
    if not user:
        raise ValueError("El usuario padre no existe")
    
    obj = Hijo(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, obj: Hijo, payload) -> Hijo:
    """Actualiza información de un hijo."""
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, obj: Hijo) -> None:
    """Elimina un hijo (hard delete)."""
    db.delete(obj)
    db.commit()
