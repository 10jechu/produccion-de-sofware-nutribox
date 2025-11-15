from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.models.address import Direccion
from app.db.models.core_models import Usuario

def list_by_user(db: Session, usuario_id: int) -> list[Direccion]:
    return db.scalars(select(Direccion).where(Direccion.usuario_id == usuario_id)).all()

def get_by_id(db: Session, direccion_id: int) -> Direccion | None:
    return db.get(Direccion, direccion_id)

def create(db: Session, payload) -> Direccion:
    user = db.get(Usuario, payload.usuario_id)
    if not user:
        raise ValueError("Usuario no existe")
    
    # --- CORRECCIÓN DE LÓGICA DE MEMBRESÍA ---
    limite = user.membresia.max_direcciones if user.membresia else 0
    
    # Si el límite es 0 (Plan Básico/Free), no permitir crear.
    if limite == 0:
        raise PermissionError("Tu plan actual no permite registrar direcciones.")

    count = db.scalar(select(func.count()).select_from(Direccion).where(Direccion.usuario_id == payload.usuario_id))
    
    # Si el límite es > 0, verificar que no se haya alcanzado.
    if count >= limite:
        raise PermissionError(f"Límite de direcciones alcanzado ({limite}).")
    # --- FIN DE LA CORRECCIÓN ---

    obj = Direccion(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def update(db: Session, obj: Direccion, payload) -> Direccion:
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

def delete(db: Session, obj: Direccion) -> None:
    db.delete(obj); db.commit()
