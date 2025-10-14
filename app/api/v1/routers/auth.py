
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import create_access_token
from app.db.schemas.auth import Token, UserRegister
from app.db.models.core_models import Rol, Membresia, Usuario
from app.core.security import get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# Helpers locales para asegurar rol/membresía
def _get_or_create_role(db: Session, nombre: str) -> Rol:
    rol = db.query(Rol).filter_by(nombre=nombre).first()
    if not rol:
        rol = Rol(nombre=nombre)
        db.add(rol); db.commit(); db.refresh(rol)
    return rol

def _get_or_create_membership(db: Session, tipo: str) -> Membresia:
    mem = db.query(Membresia).filter_by(tipo=tipo).first()
    if not mem:
        # Lógica simple de límites por tipo (ajústalo si usas otra regla)
        max_dir = 1 if tipo.lower() == "free" else 3
        mem = Membresia(tipo=tipo, max_direcciones=max_dir)
        db.add(mem); db.commit(); db.refresh(mem)
    return mem

@router.post("/register", summary="Register")
def register(payload: UserRegister, db: Session = Depends(get_db)):
    # Validar unicidad de email
    if db.query(Usuario).filter_by(email=payload.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    rol = _get_or_create_role(db, payload.rol)
    mem = _get_or_create_membership(db, payload.membresia)

    u = Usuario(
        nombre=payload.nombre,
        email=payload.email,
        hash_password=get_password_hash(payload.password),
        rol_id=rol.id,
        membresia_id=mem.id,
        activo=True,
    )
    db.add(u); db.commit(); db.refresh(u)
    return {"id": u.id, "email": u.email}

@router.post("/login", response_model=Token, summary="Login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # En nuestro flujo el "username" es el email
    user = db.query(Usuario).filter_by(email=form.username).first()
    if not user or not verify_password(form.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
