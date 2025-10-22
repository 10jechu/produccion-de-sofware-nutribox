from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.deps import get_session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.schemas.auth import Token, UserRegister
from app.db.models.core_models import Rol, Membresia, Usuario

router = APIRouter(prefix="/auth", tags=["auth"])

def _get_or_create_role(db: Session, nombre: str) -> Rol:
    rol = db.query(Rol).filter_by(nombre=nombre).first()
    if not rol:
        rol = Rol(nombre=nombre)
        db.add(rol); db.commit(); db.refresh(rol)
    return rol

def _get_or_create_membership(db: Session, tipo: str) -> Membresia:
    mem = db.query(Membresia).filter_by(tipo=tipo).first()
    if not mem:
        max_dir = 1 if (tipo or "").lower() == "free" else 3
        mem = Membresia(tipo=tipo, max_direcciones=max_dir)
        db.add(mem); db.commit(); db.refresh(mem)
    return mem

@router.post("/register", summary="Register", status_code=201)
async def register(
    request: Request,
    db: Session = Depends(get_session),
    payload: UserRegister | None = Body(default=None)  # mantiene schema en Swagger
):
    # 1) Obtener datos (JSON o FORM). Si Swagger envía JSON, payload ya viene.
    if payload is None:
        try:
            raw = await request.json()
        except Exception:
            form = await request.form()
            raw = dict(form)
        payload = UserRegister.model_validate(raw)

    # 2) Unicidad
    if db.query(Usuario).filter_by(email=payload.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # 3) Referencias
    rol = _get_or_create_role(db, payload.rol)
    mem = _get_or_create_membership(db, payload.membresia)

    # 4) Crear usuario (mapeo full_name -> columna 'nombre')
    u = Usuario(
        nombre=payload.full_name,
        email=payload.email,
        hash_password=get_password_hash(payload.password),
        rol_id=rol.id,
        membresia_id=mem.id,
        activo=True,
    )
    db.add(u)
    try:
        db.commit()
        db.refresh(u)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar usuario")

    return {"id": u.id, "email": u.email}

@router.post("/login", response_model=Token, summary="Login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.query(Usuario).filter_by(email=form.username).first()
    if not user or not verify_password(form.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
