from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.lunchbox import Lonchera, LoncheraAlimento
from app.db.models.alimento import Alimento
from app.db.models.core_models import Hijo, Usuario
from app.db.models.address import Direccion
from app.db.schemas.lunchbox import (
    LoncheraCreate, LoncheraUpdate, LoncheraItemCreate, LoncheraItemUpdate,
    LoncheraItemRead, DireccionMini
)

def list_(db: Session, hijo_id: int | None = None) -> list[Lonchera]:
    stmt = select(Lonchera)
    if hijo_id:
        stmt = stmt.where(Lonchera.hijo_id == hijo_id)
    return db.scalars(stmt).all()

def get_by_id(db: Session, lunchbox_id: int) -> Lonchera | None:
    return db.get(Lonchera, lunchbox_id)

def create(db: Session, payload: LoncheraCreate) -> Lonchera:
    if not db.get(Hijo, payload.hijo_id):
        raise ValueError("Hijo no existe")
    if payload.direccion_id and not db.get(Direccion, payload.direccion_id):
        raise ValueError("Dirección no existe")
    obj = Lonchera(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def update(db: Session, obj: Lonchera, payload: LoncheraUpdate) -> Lonchera:
    data = payload.model_dump(exclude_none=True)
    if "hijo_id" in data and not db.get(Hijo, data["hijo_id"]):
        raise ValueError("Hijo no existe")
    if "direccion_id" in data and data["direccion_id"] is not None and not db.get(Direccion, data["direccion_id"]):
        raise ValueError("Dirección no existe")
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

def add_item(db: Session, lunchbox_id: int, item: LoncheraItemCreate) -> None:
    lb = db.get(Lonchera, lunchbox_id)
    if not lb: raise LookupError("Lonchera no existe")
    if not db.get(Alimento, item.alimento_id): raise LookupError("Alimento no existe")
    exists = db.scalar(select(LoncheraAlimento).where(
        (LoncheraAlimento.lonchera_id == lunchbox_id) &
        (LoncheraAlimento.alimento_id == item.alimento_id)))
    if exists: raise ValueError("El alimento ya está en la lonchera")
    rel = LoncheraAlimento(lonchera_id=lunchbox_id, alimento_id=item.alimento_id, cantidad=item.cantidad)
    db.add(rel); db.commit()

def update_item(db: Session, lunchbox_id: int, alimento_id: int, payload: LoncheraItemUpdate) -> None:
    rel = db.scalar(select(LoncheraAlimento).where(
        (LoncheraAlimento.lonchera_id == lunchbox_id) &
        (LoncheraAlimento.alimento_id == alimento_id)))
    if not rel: raise LookupError("Item no existe")
    rel.cantidad = payload.cantidad
    db.commit()

def remove_item(db: Session, lunchbox_id: int, alimento_id: int) -> None:
    rel = db.scalar(select(LoncheraAlimento).where(
        (LoncheraAlimento.lonchera_id == lunchbox_id) &
        (LoncheraAlimento.alimento_id == alimento_id)))
    if not rel: raise LookupError("Item no existe")
    db.delete(rel); db.commit()

def list_items(db: Session, lunchbox_id: int) -> list[LoncheraItemRead]:
    rows = db.execute(
        select(LoncheraAlimento.alimento_id, Alimento.nombre, LoncheraAlimento.cantidad)
        .join(Alimento, Alimento.id == LoncheraAlimento.alimento_id)
        .where(LoncheraAlimento.lonchera_id == lunchbox_id)
    ).all()
    return [LoncheraItemRead(alimento_id=r[0], nombre=r[1], cantidad=r[2]) for r in rows]

def get_detail(db: Session, lunchbox_id: int) -> dict | None:
    lb = db.get(Lonchera, lunchbox_id)
    if not lb: return None
    items = list_items(db, lunchbox_id)

    # Dirección: usa la seleccionada en lonchera; si no, primera del usuario
    direccion = None
    if lb.direccion_id:
        d = db.get(Direccion, lb.direccion_id)
        if d:
            direccion = DireccionMini(etiqueta=d.etiqueta, direccion=d.direccion, ciudad=d.ciudad)
    else:
        hijo = db.get(Hijo, lb.hijo_id)
        if hijo:
            usuario = db.get(Usuario, hijo.usuario_id)
            if usuario:
                d = db.scalar(select(Direccion).where(Direccion.usuario_id == usuario.id))
                if d:
                    direccion = DireccionMini(etiqueta=d.etiqueta, direccion=d.direccion, ciudad=d.ciudad)

    return {
        "id": lb.id,
        "hijo_id": lb.hijo_id,
        "fecha": lb.fecha,
        "estado": lb.estado,
        "direccion_id": lb.direccion_id,
        "items": [i.model_dump() for i in items],
        "direccion": direccion.model_dump() if direccion else None
    }
