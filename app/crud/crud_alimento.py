from sqlalchemy.orm import Session
from app.db.models.alimento import Alimento
from app.db.schemas.alimento import AlimentoCreate, AlimentoUpdate

def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Alimento).filter(Alimento.activo == True).offset(skip).limit(limit).all()

def get_by_id(db: Session, alimento_id: int):
    return db.query(Alimento).filter(Alimento.id == alimento_id).first()

def create(db: Session, alimento: AlimentoCreate):
    db_alimento = Alimento(**alimento.model_dump())
    db.add(db_alimento)
    db.commit()
    db.refresh(db_alimento)
    return db_alimento

def update(db: Session, alimento_id: int, alimento: AlimentoUpdate):
    db_alimento = get_by_id(db, alimento_id)
    if not db_alimento:
        return None
    update_data = alimento.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_alimento, key, value)
    db.commit()
    db.refresh(db_alimento)
    return db_alimento

def delete(db: Session, alimento_id: int):
    db_alimento = get_by_id(db, alimento_id)
    if db_alimento:
        db_alimento.activo = False  # Soft delete
        db.commit()
    return db_alimento
