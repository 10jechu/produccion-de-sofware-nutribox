from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.core_models import Usuario, Rol, Membresia
from app.core.security import get_password_hash

def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    """Lista todos los usuarios con paginación."""
    return db.scalars(select(Usuario).offset(skip).limit(limit)).all()

def get_by_id(db: Session, user_id: int) -> Usuario | None:
    """Obtiene un usuario por ID."""
    return db.get(Usuario, user_id)

def get_by_email(db: Session, email: str) -> Usuario | None:
    """Obtiene un usuario por email."""
    return db.scalar(select(Usuario).where(Usuario.email == email))

def update(db: Session, obj: Usuario, payload) -> Usuario:
    """Actualiza un usuario."""
    data = payload.model_dump(exclude_none=True)
    
    # Validar email único si se está cambiando
    if "email" in data and data["email"] != obj.email:
        existing = get_by_email(db, data["email"])
        if existing:
            raise ValueError("El email ya está registrado")
    
    for k, v in data.items():
        setattr(obj, k, v)
    
    db.commit()
    db.refresh(obj)
    return obj

def deactivate(db: Session, obj: Usuario) -> None:
    """Desactiva un usuario (soft delete)."""
    obj.activo = False
    db.commit()

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
        hash_password=get_password_hash(password),
        rol_id=rol.id,
        membresia_id=mem.id,
    )
    db.add(u); db.commit(); db.refresh(u)
    return u

def authenticate(db: Session, email: str, password: str) -> Usuario | None:
    # tu lógica actual de auth…
    ...
