from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.db.session import get_session
from app.db.models.usuario import Usuario
from app.schemas.usuario import UsuarioLogin

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login")
def login(payload: UsuarioLogin, db: Session = Depends(get_session)):
    # Busca por correo (ajusta el campo si en tu modelo es distinto)
    user = db.query(Usuario).filter_by(email=payload.correo).first()
    if not user or not bcrypt.verify(payload.contrasena, user.hash_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    # Devuelve un token dummy por ahora para no romper el flujo
    return {"access_token": "dummy-token", "token_type": "bearer"}
