from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import bcrypt
from jose import jwt, JWTError

from app.core.config import settings

# -------------------------
# Contraseñas (bcrypt)
# -------------------------

def _to_bytes_max72(password) -> bytes:
    # bcrypt acepta máximo 72 bytes; normalizamos y truncamos
    if password is None:
        password = ""
    if not isinstance(password, str):
        password = str(password)
    return password.encode("utf-8")[:72]

def hash_password(password: str) -> str:
    pw = _to_bytes_max72(password)
    return bcrypt.hashpw(pw, bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw = _to_bytes_max72(plain_password)
    try:
        return bcrypt.checkpw(pw, hashed_password.encode("utf-8"))
    except Exception:
        return False

# -------------------------
# Tokens (JWT)
# -------------------------

SECRET_KEY: str = getattr(settings, "SECRET_KEY", None) or "dev-secret-change-me"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 horas por defecto

def create_access_token(
    subject: str | int,
    extra: Dict[str, Any] | None = None,
    expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": str(subject),
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    """Decodifica y valida un JWT. Lanza JWTError si es inválido/expirado."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        # Re-levanta para que FastAPI devuelva 401 desde la dependencia que lo use
        raise e
