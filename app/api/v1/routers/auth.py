# app/api/v1/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload # Asegúrate de importar joinedload
from app.core.deps import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.schemas.auth import Token, UserRegister # Asegúrate que UserRegister venga de schemas.auth
from app.db.models.core_models import Rol, Membresia, Usuario

router = APIRouter(prefix="/auth", tags=["auth"])

# --- Funciones Auxiliares ---
# (Asegúrate de que estas funciones estén presentes si las comentaste antes)
def _get_or_create_role(db: Session, nombre: str = "Usuario") -> Rol:
    rol = db.query(Rol).filter_by(nombre=nombre).first()
    if not rol:
        rol = Rol(nombre=nombre)
        db.add(rol); db.commit(); db.refresh(rol)
    return rol

def _get_or_create_membership(db: Session, tipo: str) -> Membresia:
    mem = db.query(Membresia).filter_by(tipo=tipo).first()
    if not mem:
        max_dir = 0 # Default para 'Free' u otros desconocidos
        if tipo.lower() == "premium":
            max_dir = 3
        elif tipo.lower() == "estandar": # O 'Estandar' si así lo tienes
             max_dir = 1
        mem = Membresia(tipo=tipo, max_direcciones=max_dir)
        db.add(mem); db.commit(); db.refresh(mem)
    return mem

# --- Endpoint de Registro ---
@router.post("/register", summary="Register")
def register(payload: UserRegister, db: Session = Depends(get_db)):
    # Validar unicidad de email
    if db.query(Usuario).filter_by(email=payload.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Rol fijo: Usuario
    rol = _get_or_create_role(db, "Usuario")
    # Membresía basada en selección
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
    # Devuelve algo simple o el ID/email si lo necesitas en el frontend post-registro
    return {"message": "Usuario registrado exitosamente", "user_id": u.id, "email": u.email}


# --- Endpoint de Login (Restaurado) ---
@router.post("/login/", response_model=Token, summary="Login") # Mantiene el slash final
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Carga el usuario y su relación 'rol' para evitar N+1 queries
    user = db.query(Usuario).options(joinedload(Usuario.rol)).filter(Usuario.email == form.username).first()

    # Verifica si el usuario existe y la contraseña es correcta
    if not user or not verify_password(form.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Verifica si el usuario está activo
    if not user.activo:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",
        )

    # Prepara los datos para incluir en el token JWT
    token_data = {
        "sub": str(user.id),  # 'sub' es el estándar para el ID del sujeto
        "email": user.email,
        # Incluye el nombre del rol, o 'Usuario' por defecto si no tiene rol asignado
        "rol": user.rol.nombre if user.rol else "Usuario"
    }
    # Crea el token de acceso
    access_token = create_access_token(token_data)

    # Devuelve el token en el formato esperado
    return {"access_token": access_token, "token_type": "bearer"}