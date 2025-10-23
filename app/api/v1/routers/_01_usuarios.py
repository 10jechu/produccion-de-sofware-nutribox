from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.core_models import Usuario
from app.schemas.usuario import UsuarioRead

router = APIRouter(prefix="/api/v1/usuarios", tags=["01 - Usuarios"])

@router.get("/", response_model=list[UsuarioRead])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.get("/{id}", response_model=UsuarioRead)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    user = db.get(Usuario, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
