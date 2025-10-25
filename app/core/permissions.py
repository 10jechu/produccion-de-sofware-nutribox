"""
Sistema de permisos por membresía y rol
Valida qué acciones puede realizar cada usuario según su plan
"""
from fastapi import HTTPException, status
from app.db.models.core_models import Usuario


class PermissionDenied(HTTPException):
    def __init__(self, message: str = "No tienes permisos para esta acción"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


def require_membership(user: Usuario, required_plans: list[str]) -> None:
    """
    Valida que el usuario tenga uno de los planes requeridos

    Args:
        user: Usuario autenticado
        required_plans: Lista de planes permitidos ['Premium', 'Estandar', 'Free']

    Raises:
        PermissionDenied: Si el usuario no tiene el plan requerido
    """
    if not user.membresia:
        raise PermissionDenied("Usuario sin membresía asignada")

    if user.membresia.tipo not in required_plans:
        raise PermissionDenied(
            f"Esta funcionalidad requiere plan {' o '.join(required_plans)}. "
            f"Tu plan actual: {user.membresia.tipo}"
        )


def require_admin(user: Usuario) -> None:
    """
    Valida que el usuario sea Administrador

    Args:
        user: Usuario autenticado

    Raises:
        PermissionDenied: Si el usuario no es admin
    """
    if not user.rol or user.rol.nombre != "Admin":
        raise PermissionDenied("Solo administradores pueden realizar esta acción")


def can_add_lunchbox_to_profile(user: Usuario) -> bool:
    """
    Verifica si el usuario puede agregar loncheras predeterminadas

    Returns:
        True si es Estándar o Premium
    """
    if not user.membresia:
        return False
    return user.membresia.tipo in ["Estandar", "Premium"]


def can_customize_lunchbox(user: Usuario) -> bool:
    """
    Verifica si el usuario puede personalizar loncheras (alimento por alimento)

    Returns:
        True solo si es Premium
    """
    if not user.membresia:
        return False
    return user.membresia.tipo == "Premium"


def can_manage_foods(user: Usuario) -> bool:
    """
    Verifica si puede gestionar alimentos (CRUD)

    Returns:
        True si es Admin o Premium
    """
    if not user.rol or not user.membresia:
        return False
    return user.rol.nombre == "Admin" or user.membresia.tipo == "Premium"


def can_configure_restrictions(user: Usuario) -> bool:
    """
    Verifica si puede configurar restricciones alimentarias

    Returns:
        True si es Estándar o Premium
    """
    if not user.membresia:
        return False
    return user.membresia.tipo in ["Estandar", "Premium"]


def can_view_advanced_stats(user: Usuario) -> bool:
    """
    Verifica si puede ver estadísticas avanzadas

    Returns:
        True solo si es Premium
    """
    if not user.membresia:
        return False
    return user.membresia.tipo == "Premium"


def get_max_addresses(user: Usuario) -> int:
    """
    Obtiene el límite de direcciones según membresía

    Returns:
        0 para Free, 1 para Estándar, 3 para Premium
    """
    if not user.membresia:
        return 0
    return user.membresia.max_direcciones


def validate_address_limit(user: Usuario, current_count: int) -> None:
    """
    Valida que no se exceda el límite de direcciones

    Args:
        user: Usuario autenticado
        current_count: Cantidad actual de direcciones

    Raises:
        PermissionDenied: Si se excede el límite
    """
    max_allowed = get_max_addresses(user)

    if max_allowed == 0:
        raise PermissionDenied("El plan Free no permite gestionar direcciones")

    if current_count >= max_allowed:
        raise PermissionDenied(
            f"Límite de direcciones alcanzado ({max_allowed}). "
            f"Actualiza tu plan para agregar más direcciones."
        )


# Matriz de permisos por funcionalidad
PERMISSIONS_MATRIX = {
    "view_menus": ["Free", "Estandar", "Premium"],
    "add_predetermined_lunchbox": ["Estandar", "Premium"],
    "remove_predetermined_lunchbox": ["Estandar", "Premium"],
    "customize_lunchbox": ["Premium"],
    "manage_foods": ["Premium"],  # Usuario Premium (Admin siempre puede)
    "configure_restrictions": ["Estandar", "Premium"],
    "manage_addresses": ["Estandar", "Premium"],
    "view_basic_stats": ["Estandar", "Premium"],
    "view_advanced_stats": ["Premium"],
    "history_and_restore": ["Premium"],
}


def has_permission(user: Usuario, action: str) -> bool:
    """
    Verifica si el usuario tiene permiso para una acción específica

    Args:
        user: Usuario autenticado
        action: Clave de la acción (ver PERMISSIONS_MATRIX)

    Returns:
        True si tiene permiso
    """
    # Admin siempre tiene todos los permisos
    if user.rol and user.rol.nombre == "Admin":
        return True

    if action not in PERMISSIONS_MATRIX:
        return False

    if not user.membresia:
        return False

    return user.membresia.tipo in PERMISSIONS_MATRIX[action]