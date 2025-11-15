from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import verify_token
from app.db.models.core_models import Usuario

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> Usuario:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    user = db.query(Usuario).filter(Usuario.id == int(payload.get("sub"))).first()
    if not user or not user.activo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado o inactivo")
    
    return user

def get_current_admin_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if current_user.rol.nombre != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se requieren permisos de administrador")
    return current_user

def get_current_premium_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    "Verifica que el usuario tenga membresía Premium"
    print(f"🔍 DEBUG: Verificando membresía - Usuario: {current_user.email}, Membresía: {current_user.membresia.tipo}")
    
    # Solo permitir si es Premium (no Admin)
    if current_user.membresia.tipo != "Premium":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Se requiere plan Premium para acceder a esta función. Tu plan actual: {current_user.membresia.tipo}"
        )
    return current_user

def get_current_estandar_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    "Verifica que el usuario tenga membresía Estándar o Premium"
    if current_user.membresia.tipo not in ["Estandar", "Premium"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se requiere plan Estándar o Premium para acceder a esta función")
    return current_user

def get_current_free_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    "Verifica que el usuario tenga membresía Free"
    if current_user.membresia.tipo != "Free":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Esta función es solo para usuarios Free")
    return current_user
