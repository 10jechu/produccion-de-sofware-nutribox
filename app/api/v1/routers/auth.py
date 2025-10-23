from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from pydantic import BaseModel, EmailStr
from app.db.models.rol import Rol
from app.db.models.membresia import Membresia
from app.db.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["auth"])

# Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    rol: str = "Usuario"
    membresia: str = "Basico"

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
        max_dir = 1 if tipo.lower() in ["basico", "free"] else (2 if tipo.lower() == "estandar" else 3)
        mem = Membresia(tipo=tipo, max_direcciones=max_dir)
        db.add(mem)
        db.commit()
        db.refresh(mem)
    return mem

@router.post("/register", summary="Register User", status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    if db.query(Usuario).filter_by(email=payload.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Obtener o crear rol y membresía
    rol = _get_or_create_role(db, payload.rol)
    mem = _get_or_create_membership(db, payload.membresia)

    # Crear usuario
    u = Usuario(
        nombre=payload.full_name,
        email=payload.email,
        hash_password=get_password_hash(payload.password),
        rol_id=rol.id,
        membresia_id=mem.id,
        activo=True,
        estado="activo"
    )
    db.add(u)
    try:
        db.commit()
        db.refresh(u)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar usuario: {str(e)}")

    return {"id": u.id, "email": u.email, "nombre": u.nombre}

@router.post("/login", response_model=Token, summary="Login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter_by(email=form.username).first()
    if not user or not verify_password(form.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales inválidas"
        )
    
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
