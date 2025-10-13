from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.lunchbox import Lonchera, LoncheraAlimento
from app.db.models.alimento import Alimento
from app.db.models.core_models import Hijo
from app.db.schemas.lunchbox import LoncheraCreate, LoncheraItemCreate

def list_(db: Session, hijo_id: int | None = None) -> list[Lonchera]:
    stmt = select(Lonchera)
    if hijo_id:
        stmt = stmt.where(Lonchera.hijo_id == hijo_id)
    return db.scalars(stmt).all()

def create(db: Session, payload: LoncheraCreate) -> Lonchera:
    # valida hijo
    if not db.get(Hijo, payload.hijo_id):
        raise ValueError("Hijo no existe")
    obj = Lonchera(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def add_item(db: Session, lunchbox_id: int, item: LoncheraItemCreate) -> None:
    lb = db.get(Lonchera, lunchbox_id)
    if not lb:
        raise LookupError("Lonchera no existe")
    if not db.get(Alimento, item.alimento_id):
        raise LookupError("Alimento no existe")
    exists = db.scalar(
        select(LoncheraAlimento).where(
            (LoncheraAlimento.lonchera_id == lunchbox_id) &
            (LoncheraAlimento.alimento_id == item.alimento_id)
        )
    )
    if exists:
        raise ValueError("El alimento ya está en la lonchera")
    rel = LoncheraAlimento(lonchera_id=lunchbox_id, alimento_id=item.alimento_id, cantidad=item.cantidad)
    db.add(rel); db.commit()

def remove_item(db: Session, lunchbox_id: int, alimento_id: int) -> None:
    rel = db.scalar(
        select(LoncheraAlimento).where(
            (LoncheraAlimento.lonchera_id == lunchbox_id) &
            (LoncheraAlimento.alimento_id == alimento_id)
        )
    )
    if not rel:
        raise LookupError("Item no existe")
    db.delete(rel); db.commit()
