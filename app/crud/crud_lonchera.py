from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.lonchera import Lonchera, LoncheraAlimento
from app.db.models.alimento import Alimento
from app.db.schemas.lonchera import LoncheraCreate, LoncheraUpdate, LoncheraItemCreate

def get_all(db: Session, hijo_id: int | None = None):
    query = db.query(Lonchera)
    if hijo_id:
        query = query.filter(Lonchera.hijo_id == hijo_id)
    return query.all()

def get_by_id(db: Session, lonchera_id: int):
    return db.query(Lonchera).filter(Lonchera.id == lonchera_id).first()

def create(db: Session, lonchera: LoncheraCreate):
    db_lonchera = Lonchera(**lonchera.model_dump())
    db.add(db_lonchera)
    db.commit()
    db.refresh(db_lonchera)
    return db_lonchera

def update(db: Session, lonchera_id: int, lonchera: LoncheraUpdate):
    db_lonchera = get_by_id(db, lonchera_id)
    if not db_lonchera:
        return None
    update_data = lonchera.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lonchera, key, value)
    db.commit()
    db.refresh(db_lonchera)
    return db_lonchera

def delete(db: Session, lonchera_id: int):
    db_lonchera = get_by_id(db, lonchera_id)
    if db_lonchera:
        db.delete(db_lonchera)
        db.commit()
    return db_lonchera

def add_item(db: Session, lonchera_id: int, item: LoncheraItemCreate):
    # Verificar si ya existe
    existing = db.query(LoncheraAlimento).filter(
        LoncheraAlimento.lonchera_id == lonchera_id,
        LoncheraAlimento.alimento_id == item.alimento_id
    ).first()
    
    if existing:
        existing.cantidad += item.cantidad
        db.commit()
        db.refresh(existing)
        return existing
    
    db_item = LoncheraAlimento(
        lonchera_id=lonchera_id,
        alimento_id=item.alimento_id,
        cantidad=item.cantidad
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_item(db: Session, lonchera_id: int, alimento_id: int):
    item = db.query(LoncheraAlimento).filter(
        LoncheraAlimento.lonchera_id == lonchera_id,
        LoncheraAlimento.alimento_id == alimento_id
    ).first()
    if item:
        db.delete(item)
        db.commit()
    return item

def get_items(db: Session, lonchera_id: int):
    return db.query(LoncheraAlimento).filter(
        LoncheraAlimento.lonchera_id == lonchera_id
    ).all()
