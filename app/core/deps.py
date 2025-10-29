from app.db.database import get_db
__all__ = ["get_db"]


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.db.database import SessionLocal
from app.db.models.core_models import Usuario
from app.db.models.core_models import Rol

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")

def get_current_user(token: str = Depends(oauth2_scheme)) -> Usuario:
    data = decode_token(token)
    if not data or "sub" not in data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    db = SessionLocal()
    try:
        user = db.get(Usuario, int(data["sub"]))
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return user
    finally:
        db.close()

def require_admin(current_user: Usuario = Depends(get_current_user), db: SessionLocal = Depends(get_db)) -> Usuario:
    """
    Dependencia que verifica si el usuario actual tiene el rol 'Admin'.
    Si no lo tiene, lanza una excepción HTTP 403 Forbidden.
    """
    # Es más seguro cargar el rol explícitamente si no viene en el token
    # o si quieres revalidar contra la BD
    user_with_role = db.query(Usuario).options(joinedload(Usuario.rol)).filter(Usuario.id == current_user.id).first()

    if not user_with_role or not user_with_role.rol or user_with_role.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operación no permitida. Se requiere rol de Administrador."
        )
    return current_user # Devuelve el usuario si la verificación pasa

# Asegúrate de añadir joinedload si no está
from sqlalchemy.orm import joinedload
