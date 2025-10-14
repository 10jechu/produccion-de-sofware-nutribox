from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.db.models.restriction import Restriccion

def list_(db: Session, hijo_id: int | None = None) -> list[Restriccion]:
    stmt = select(Restriccion)
    if hijo_id:
        stmt = stmt.where(Restriccion.hijo_id == hijo_id)
    return db.scalars(stmt).all()

def get(db: Session, restriccion_id: int) -> Restriccion | None:
    return db.get(Restriccion, restriccion_id)

def create(db: Session, payload) -> Restriccion:
    if payload.tipo not in {"alergia", "prohibido"}:
        raise ValueError("tipo inválido (use 'alergia' o 'prohibido')")
    if payload.tipo == "alergia" and not payload.alimento_id:
        raise ValueError("alergia requiere alimento_id")
    if payload.tipo == "prohibido" and not (payload.texto and payload.texto.strip()):
        raise ValueError("prohibido requiere texto")
    obj = Restriccion(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def update(db: Session, restriccion_id: int, payload) -> Restriccion:
    obj = db.get(Restriccion, restriccion_id)
    if not obj:
        raise LookupError("No existe")

    data = payload.model_dump(exclude_unset=True)
    # valores efectivos después del patch
    tipo = data.get("tipo", obj.tipo)
    alimento_id = data.get("alimento_id", obj.alimento_id)
    texto = data.get("texto", obj.texto)

    if tipo not in {"alergia", "prohibido"}:
        raise ValueError("tipo inválido (use 'alergia' o 'prohibido')")
    if tipo == "alergia" and not alimento_id:
        raise ValueError("alergia requiere alimento_id")
    if tipo == "prohibido" and not (texto and str(texto).strip()):
        raise ValueError("prohibido requiere texto")

    # --- Duplicados (post-merge de datos) ---
    if tipo == "alergia":
        dup = db.scalar(
            select(Restriccion).where(
                (Restriccion.hijo_id == obj.hijo_id) &
                (Restriccion.tipo == "alergia") &
                (Restriccion.alimento_id == alimento_id) &
                (Restriccion.id != obj.id)
            )
        )
        if dup:
            raise ValueError("Esta alergia ya está registrada para el hijo")
    elif tipo == "prohibido":
        dup = db.scalar(
            select(Restriccion).where(
                (Restriccion.hijo_id == obj.hijo_id) &
                (Restriccion.tipo == "prohibido") &
                (Restriccion.texto == texto) &
                (Restriccion.id != obj.id)
            )
        )
        if dup:
            raise ValueError("Esta restricción de 'prohibido' ya existe para el hijo")

    obj.tipo = tipo
    obj.alimento_id = alimento_id
    obj.texto = texto
    db.commit(); db.refresh(obj)
    return obj

def delete(db: Session, restriccion_id: int) -> None:
    obj = db.get(Restriccion, restriccion_id)
    if not obj:
        raise LookupError("No existe")
    db.delete(obj); db.commit()
