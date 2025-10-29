# <<<<<<<<<< COMIENZA CÓDIGO para el NUEVO archivo: app/core/security_deps.py >>>>>>>>>>

from fastapi import Depends, HTTPException, status
from app.db.models.core_models import Usuario, Rol, Membresia # Importa modelos necesarios

# IMPORTANTE: Importa get_current_user desde el archivo original deps.py
from app.core.deps import get_current_user

# --- Dependencia para verificar si el usuario es Administrador ---
def get_current_admin_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if not current_user.rol or current_user.rol.nombre != "Admin": # Cambia 'Admin' si es necesario
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acción permitida solo para administradores"
        )
    return current_user

# --- Dependencia para verificar si es Usuario Principal (Padre/Madre) ---
# (Opcional, si la necesitas)
def get_current_principal_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    allowed_roles = {"Usuario Principal", "Usuario"} # Ajusta según tu BD
    if not current_user.rol or current_user.rol.nombre not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acción permitida solo para usuarios principales (Padres/Madres)"
        )
    return current_user

# --- Dependencia Fábrica para verificar Membresía Mínima ---
def require_membership(required_level: str):
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

# <<<<<<<<<< FIN CÓDIGO para app/core/security_deps.py >>>>>>>>>>