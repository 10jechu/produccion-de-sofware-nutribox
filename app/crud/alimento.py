from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.alimento import Alimento
from app.db.schemas.food import AlimentoCreate, AlimentoUpdate

def list_(db: Session, only_active: bool | str = True) -> list[Alimento]:
    stmt = select(Alimento)
    if only_active == "all":
        pass  # Retorna todos
    elif only_active is True or only_active == "true":
        stmt = stmt.where(Alimento.activo == True)
    elif only_active is False or only_active == "false":
        stmt = stmt.where(Alimento.activo == False)
    return db.scalars(stmt).all()

def get_by_id(db: Session, alimento_id: int) -> Alimento | None:
    return db.get(Alimento, alimento_id)

def exists_by_name(db: Session, nombre: str) -> bool:
    return db.scalar(select(Alimento).where(Alimento.nombre == nombre)) is not None

def create(db: Session, payload: AlimentoCreate) -> Alimento:
    obj = Alimento(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def update(db: Session, obj: Alimento, payload: AlimentoUpdate) -> Alimento:
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

def soft_delete(db: Session, obj: Alimento) -> None:
    obj.activo = False
    db.commit()
