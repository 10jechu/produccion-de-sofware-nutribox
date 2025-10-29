# app/core/deps.py (VERSIÓN FINAL Y CORREGIDA)

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Generator 
# Importa los modelos core
from app.db.models.core_models import Usuario, Rol, Membresia
# 🛑 CORRECCIÓN CRÍTICA: Importar la sesión desde la ruta correcta
from app.db.database import SessionLocal 


# ----------------------------------------------------
# 1. FUNCIÓN BÁSICA DE BASE DE DATOS (get_db)
# ----------------------------------------------------

def get_db() -> Generator:
    """Proporciona una sesión de base de datos a los endpoints."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ----------------------------------------------------
# 2. FUNCIÓN DE USUARIO AUTENTICADO (get_current_user)
# ----------------------------------------------------
# ⚠️ Importante: Asumimos que la lógica para obtener el usuario del token 
# está definida en otro lugar (ej., app/core/security.py)

# Este es el placeholder para la dependencia
def get_current_user(db: Session = Depends(get_db)) -> Usuario:
    """Placeholder para obtener el usuario del Token JWT."""
    # Aquí iría la lógica para decodificar el token y buscar el usuario en la DB.
    
    # Si la lógica de seguridad falla o no hay token válido
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o no proporcionado",
        headers={"WWW-Authenticate": "Bearer"},
    )


# ----------------------------------------------------
# 3. DEPENDENCIAS DE ROL Y MEMBRESÍA (Seguridad Fase II/III)
# ----------------------------------------------------

# Dependencia para verificar si el usuario es Administrador
def get_current_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Verifica si el usuario actual tiene el rol 'Admin'."""
    if not current_user.rol or current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acción permitida solo para administradores"
        )
    return current_user

# Dependencia para verificar si es Usuario Principal (Padre/Madre)
def get_current_principal_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Verifica si el usuario actual tiene el rol de Padre/Madre."""
    allowed_roles = {"Usuario", "Usuario Principal"}
    if not current_user.rol or current_user.rol.nombre not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acción permitida solo para usuarios principales (Padres/Madres)"
        )
    return current_user

# Dependencia Fábrica para verificar Membresía Mínima
def require_membership(required_level: str):
    """Genera una dependencia que verifica el nivel de membresía mínimo."""
    tiers = {"Básico": 0, "Free": 0, "Estándar": 1, "Estandar": 1, "Premium": 2}

    async def _check_membership(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        user_level_name = current_user.membresia.tipo if current_user.membresia else "Free"
        user_tier = tiers.get(user_level_name, 0)
        required_tier = tiers.get(required_level, 0)

        if user_tier < required_tier:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Esta acción requiere membresía '{required_level}' o superior."
            )
        return current_user

    return _check_membership