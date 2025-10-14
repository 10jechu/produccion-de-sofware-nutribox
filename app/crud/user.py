from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.core_models import Usuario
from app.core.security import hash_password, verify_password

def get_by_email(db: Session, email: str) -> Usuario | None:
    return db.scalar(select(Usuario).where(Usuario.email == email))

def create(db: Session, nombre: str, email: str, password: str) -> Usuario:
    if get_by_email(db, email):
        raise ValueError("El email ya está registrado")
    u = Usuario(nombre=nombre, email=email, hash_password=hash_password(password))
    db.add(u); db.commit(); db.refresh(u)
    return u

def authenticate(db: Session, email: str, password: str) -> Usuario | None:
    u = get_by_email(db, email)
    if not u or not verify_password(password, u.hash_password):
        return None
    return u
