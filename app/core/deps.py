from app.db.database import get_db
__all__ = ["get_db"]


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.db.database import SessionLocal
from app.db.models.core_models import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

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
