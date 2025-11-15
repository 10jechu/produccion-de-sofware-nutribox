from app.db.database import SessionLocal
from app.core.security import verify_token  # Cambiar decode_token por verify_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mantener decode_token como alias para compatibilidad
decode_token = verify_token
