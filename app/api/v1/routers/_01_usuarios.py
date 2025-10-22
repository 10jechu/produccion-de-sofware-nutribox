from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
from passlib.context import CryptContext

from app.db.session import get_session
from app.schemas import UsuarioCreate, UsuarioRead
from app.db.models.usuario import Usuario# modelo SQLAlchemy real

router = APIRouter(prefix="/api/v1/usuarios", tags=["usuarios"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(payload: UsuarioCreate, db: Session = Depends(get_session)):
    # Normaliza datos desde schema (acepta correo/email, contrasena/password)
    email = payload.email
    nombre = payload.nombre
    hashed = pwd_context.hash(payload.password)

    # Defaults amables (si tus columnas existen y son NOT NULL)
    now = datetime.utcnow()
    extra = {}
    # agrega los defaults SOLO si esas columnas existen en el modelo
    cols = {c.name for c in Usuario.__table__.columns}
    if "created_at" in cols: extra["created_at"] = now
    if "updated_at" in cols: extra["updated_at"] = now
    if "is_active"  in cols: extra["is_active"]  = True
    if "estado"     in cols: extra["estado"]     = "activo"
    if "rol_id"     in cols: extra["rol_id"]     = 1
    if "membresia_id" in cols: extra["membresia_id"] = 1

    try:
        u = Usuario(
            nombre=nombre,
            email=email if "email" in cols else None,
            hash_password=hashed if "hash_password" in cols else None,
            **{k:v for k,v in extra.items() if k in cols}
        )
        db.add(u); db.commit(); db.refresh(u)
        return u

    except IntegrityError as e:
        db.rollback()
        # típico: UNIQUE(email) o NOT NULL de una columna extra
        raise HTTPException(status_code=400, detail=f"IntegrityError: {getattr(e, 'orig', e)}")

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"SQLAlchemyError: {e.__class__.__name__}: {e}")
