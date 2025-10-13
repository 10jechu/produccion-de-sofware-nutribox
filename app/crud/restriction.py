from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.restriction import Restriccion

def list_(db: Session, hijo_id: int | None = None) -> list[Restriccion]:
    stmt = select(Restriccion)
    if hijo_id:
        stmt = stmt.where(Restriccion.hijo_id == hijo_id)
    return db.scalars(stmt).all()

def create(db: Session, payload) -> Restriccion:
    # Validaciones básicas
    if payload.tipo not in {"alergia", "prohibido"}:
        raise ValueError("tipo inválido (use 'alergia' o 'prohibido')")
    if payload.tipo == "alergia" and not payload.alimento_id:
        raise ValueError("alergia requiere alimento_id")
    if payload.tipo == "prohibido" and not (payload.texto and payload.texto.strip()):
        raise ValueError("prohibido requiere texto")
    obj = Restriccion(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def delete(db: Session, restriccion_id: int) -> None:
    obj = db.get(Restriccion, restriccion_id)
    if not obj:
        raise LookupError("No existe")
    db.delete(obj); db.commit()
