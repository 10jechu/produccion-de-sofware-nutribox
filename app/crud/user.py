# app/crud/user.py
from sqlalchemy.orm import Session
from app.db.models.core_models import Usuario, Rol, Membresia
from app.core.security import hash_password

def _get_or_create_default_role(db: Session, nombre="Usuario") -> Rol:
    rol = db.query(Rol).filter_by(nombre=nombre).first()
    if not rol:
        rol = Rol(nombre=nombre)
        db.add(rol); db.commit(); db.refresh(rol)
    return rol

def _get_or_create_default_membership(db: Session, tipo="Free", max_dirs=3) -> Membresia:
    mem = db.query(Membresia).filter_by(tipo=tipo).first()
    if not mem:
        mem = Membresia(tipo=tipo, max_direcciones=max_dirs)
        db.add(mem); db.commit(); db.refresh(mem)
    return mem

def create(
    db: Session,
    nombre: str,
    email: str,
    password: str,
    rol_nombre: str | None = None,
    membresia_tipo: str | None = None,
) -> Usuario:
    rol = _get_or_create_default_role(db, rol_nombre or "Usuario")
    mem = _get_or_create_default_membership(db, membresia_tipo or "Free")

    u = Usuario(
        nombre=nombre,
        email=email,
        hash_password=hash_password(password),
        rol_id=rol.id,
        membresia_id=mem.id,
    )
    db.add(u); db.commit(); db.refresh(u)
    return u

def authenticate(db: Session, email: str, password: str) -> Usuario | None:
    # tu lógica actual de auth…
    ...
