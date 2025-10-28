from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.lunchbox import Lonchera, LoncheraAlimento
from app.db.models.core_models import Hijo
from app.db.models.alimento import Alimento
from app.db.models.address import Direccion
from sqlalchemy import delete as sqlalchemy_delete

def list_(db: Session, hijo_id: int | None = None) -> list[Lonchera]:
    stmt = select(Lonchera)
    if hijo_id:
        stmt = stmt.where(Lonchera.hijo_id == hijo_id)
    return db.scalars(stmt).all()

def get_by_id(db: Session, lonchera_id: int) -> Lonchera | None:
    return db.get(Lonchera, lonchera_id)

def create(db: Session, payload) -> Lonchera:
    hijo = db.get(Hijo, payload.hijo_id)
    if not hijo:
        raise ValueError("Hijo no encontrado")
    
    if payload.direccion_id:
        direccion = db.get(Direccion, payload.direccion_id)
        if not direccion:
            raise ValueError("Dirección no encontrada")
    
    obj = Lonchera(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, obj: Lonchera, payload) -> Lonchera:
    data = payload.model_dump(exclude_none=True)
    
    if "direccion_id" in data and data["direccion_id"]:
        direccion = db.get(Direccion, data["direccion_id"])
        if not direccion:
            raise ValueError("Dirección no encontrada")
    
    for k, v in data.items():
        setattr(obj, k, v)
    
    db.commit()
    db.refresh(obj)
    return obj

def list_items(db: Session, lonchera_id: int) -> list[LoncheraAlimento]:
    return db.scalars(
        select(LoncheraAlimento).where(LoncheraAlimento.lonchera_id == lonchera_id)
    ).all()

def add_item(db: Session, lonchera_id: int, item) -> None:
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise LookupError("Lonchera no encontrada")
    
    alimento = db.get(Alimento, item.alimento_id)
    if not alimento:
        raise ValueError("Alimento no encontrado")
    
    existing = db.scalar(
        select(LoncheraAlimento).where(
            LoncheraAlimento.lonchera_id == lonchera_id,
            LoncheraAlimento.alimento_id == item.alimento_id
        )
    )
    
    if existing:
        raise ValueError("Este alimento ya está en la lonchera")
    
    obj = LoncheraAlimento(
        lonchera_id=lonchera_id,
        alimento_id=item.alimento_id,
        cantidad=item.cantidad
    )
    db.add(obj)
    db.commit()

def update_item(db: Session, lonchera_id: int, alimento_id: int, payload) -> None:
    item = db.scalar(
        select(LoncheraAlimento).where(
            LoncheraAlimento.lonchera_id == lonchera_id,
            LoncheraAlimento.alimento_id == alimento_id
        )
    )
    
    if not item:
        raise LookupError("Item no encontrado en esta lonchera")
    
    item.cantidad = payload.cantidad
    db.commit()

def remove_item(db: Session, lonchera_id: int, alimento_id: int) -> None:
    item = db.scalar(
        select(LoncheraAlimento).where(
            LoncheraAlimento.lonchera_id == lonchera_id,
            LoncheraAlimento.alimento_id == alimento_id
        )
    )
    
    if not item:
        raise LookupError("Item no encontrado")
    
    db.delete(item)
    db.commit()

def delete(db: Session, lonchera_id: int) -> None:
    """Elimina una lonchera y todos sus LoncheraAlimento asociados."""
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise LookupError("Lonchera no encontrada")

    # Eliminar primero los items asociados (LoncheraAlimento)
    db.execute(
        sqlalchemy_delete(LoncheraAlimento).where(LoncheraAlimento.lonchera_id == lonchera_id)
    )

    # Luego eliminar la lonchera
    db.delete(lonchera)
    db.commit()