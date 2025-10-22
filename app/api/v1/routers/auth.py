from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.schemas.auth import Token, UserRegister
from app.db.models.core_models import Rol, Membresia, Usuario

router = APIRouter(prefix="/auth", tags=["auth"])

def _get_or_create_role(db: Session, nombre: str) -> Rol:
    rol = db.query(Rol).filter_by(nombre=nombre).first()
    if not rol:
        rol = Rol(nombre=nombre)
        db.add(rol)
        db.commit()
        db.refresh(rol)
    return rol

def _get_or_create_membership(db: Session, tipo: str) -> Membresia:
    mem = db.query(Membresia).filter_by(tipo=tipo).first()
    if not mem:
        max_dir = 1 if tipo == "Free" else 3
        mem = Membresia(tipo=tipo, max_direcciones=max_dir)
        db.add(mem)
        db.commit()
        db.refresh(mem)
    return mem

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""
    # Verificar si el email ya existe
    if db.query(Usuario).filter_by(email=payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Obtener o crear rol y membresía
    rol = _get_or_create_role(db, payload.rol)
    mem = _get_or_create_membership(db, payload.membresia)
    
    # Crear usuario
    user = Usuario(
        nombre=payload.full_name,
        email=payload.email,
        hash_password=get_password_hash(payload.password),
        rol_id=rol.id,
        membresia_id=mem.id,
        activo=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"id": user.id, "email": user.email, "message": "Usuario creado exitosamente"}

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Iniciar sesión y obtener token JWT"""
    user = db.query(Usuario).filter_by(email=form.username).first()
    
    if not user or not verify_password(form.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "email": current_user.email,
        "rol": current_user.rol.nombre,
        "membresia": current_user.membresia.tipo
    }
