from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.models.address import Direccion
from app.db.models.core_models import Usuario

def list_by_user(db: Session, usuario_id: int) -> list[Direccion]:
    return db.scalars(select(Direccion).where(Direccion.usuario_id == usuario_id)).all()

def create(db: Session, payload) -> Direccion:
    user = db.get(Usuario, payload.usuario_id)
    if not user:
        raise ValueError("Usuario no existe")
    # límite por membresía (0 = sin límite)
    limite = user.membresia.max_direcciones if user.membresia else 0
    count = db.scalar(select(func.count()).select_from(Direccion).where(Direccion.usuario_id == payload.usuario_id))
    if limite and count >= limite:
        raise PermissionError(f"Límite de direcciones alcanzado ({limite}).")
    obj = Direccion(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
