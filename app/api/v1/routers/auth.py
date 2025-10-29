from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import create_access_token
from app.db.schemas.auth import Token, UserRegister
from app.db.models.core_models import Rol, Membresia, Usuario
from app.core.security import get_password_hash, verify_password
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/auth", tags=["auth"])

# Simplificación: El sistema solo usará el Rol "Usuario"
def _get_or_create_role(db: Session, nombre: str = "Usuario") -> Rol:
    rol = db.query(Rol).filter_by(nombre=nombre).first()
    if not rol:
        rol = Rol(nombre=nombre)
        db.add(rol); db.commit(); db.refresh(rol)
    return rol

# Simplificación: Las membresías son automáticas
def _get_or_create_membership(db: Session, tipo: str) -> Membresia:
    mem = db.query(Membresia).filter_by(tipo=tipo).first()
    if not mem:
        # Lógica de límites (Básico/Estandar=1, Premium=3)
        max_dir = 3 if tipo.lower() == "premium" else 1
        mem = Membresia(tipo=tipo, max_direcciones=max_dir)
        db.add(mem); db.commit(); db.refresh(mem)
    return mem

@router.post("/register", summary="Register")
def register(payload: UserRegister, db: Session = Depends(get_db)):
    # Validar unicidad de email
    if db.query(Usuario).filter_by(email=payload.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Rol fijo: Usuario
    rol = _get_or_create_role(db, "Usuario")
    # Membresía basada en selección de usuario
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

router.post("/login", response_model=Token, summary="Login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).options(joinedload(Usuario.rol)).filter_by(email=form.username).first() # Asegura cargar el rol
    if not user or not verify_password(form.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}, # Importante para OAuth2
        )
    if not user.activo: # Añadir verificación de usuario activo
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",
        )

    # Prepara los datos para el token, incluyendo el rol
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "rol": user.rol.nombre if user.rol else "Usuario" # Incluye el rol
    }
    access_token = create_access_token(token_data)

    # Devuelve el token como antes
    return {"access_token": access_token, "token_type": "bearer"}