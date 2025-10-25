"""
Sistema de validación de restricciones alimentarias
Verifica que los alimentos de una lonchera cumplan con las restricciones del hijo
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.restriction import Restriccion
from app.db.models.alimento import Alimento
from app.db.models.core_models import Hijo


class RestrictionViolation(Exception):
    """Excepción cuando se viola una restricción alimentaria"""

    def __init__(self, message: str, alimento_nombre: str = None, restriccion_tipo: str = None):
        self.alimento_nombre = alimento_nombre
        self.restriccion_tipo = restriccion_tipo
        super().__init__(message)


def get_child_restrictions(db: Session, hijo_id: int) -> list[Restriccion]:
    """
    Obtiene todas las restricciones activas de un hijo

    Args:
        db: Sesión de base de datos
        hijo_id: ID del hijo

    Returns:
        Lista de restricciones
    """
    return db.scalars(
        select(Restriccion).where(Restriccion.hijo_id == hijo_id)
    ).all()


def check_food_against_restrictions(
        db: Session,
        hijo_id: int,
        alimento_id: int
) -> tuple[bool, str | None]:
    """
    Verifica si un alimento específico viola alguna restricción del hijo

    Args:
        db: Sesión de base de datos
        hijo_id: ID del hijo
        alimento_id: ID del alimento a verificar

    Returns:
        (es_permitido, mensaje_error)
        - (True, None) si está permitido
        - (False, "mensaje") si está bloqueado
    """
    # Obtener alimento
    alimento = db.get(Alimento, alimento_id)
    if not alimento:
        return False, "Alimento no encontrado"

    if not alimento.activo:
        return False, f"El alimento '{alimento.nombre}' está inactivo"

    # Obtener restricciones del hijo
    restricciones = get_child_restrictions(db, hijo_id)

    if not restricciones:
        return True, None  # Sin restricciones, todo permitido

    # Verificar cada restricción
    for rest in restricciones:
        # Tipo 1: Alergia a alimento específico
        if rest.tipo == "alergia" and rest.alimento_id:
            if rest.alimento_id == alimento_id:
                return False, (
                    f"🚫 ALERGIA: El niño es alérgico a '{alimento.nombre}'. "
                    f"No puede consumir este alimento."
                )

        # Tipo 2: Alimento prohibido por texto (match parcial)
        elif rest.tipo == "prohibido" and rest.texto:
            texto_busqueda = rest.texto.lower().strip()
            nombre_alimento = alimento.nombre.lower()

            if texto_busqueda in nombre_alimento or nombre_alimento in texto_busqueda:
                return False, (
                    f"🚫 PROHIBIDO: '{alimento.nombre}' contiene ingredientes prohibidos "
                    f"({rest.texto}). No puede ser incluido en la lonchera."
                )

    return True, None


def validate_lunchbox_foods(
        db: Session,
        hijo_id: int,
        alimentos_ids: list[int]
) -> tuple[bool, list[str]]:
    """
    Valida una lista completa de alimentos para una lonchera

    Args:
        db: Sesión de base de datos
        hijo_id: ID del hijo
        alimentos_ids: Lista de IDs de alimentos a validar

    Returns:
        (es_valida, lista_errores)
        - (True, []) si todos los alimentos son válidos
        - (False, ["error1", "error2"]) si hay violaciones
    """
    errores = []

    for alimento_id in alimentos_ids:
        es_permitido, mensaje = check_food_against_restrictions(db, hijo_id, alimento_id)

        if not es_permitido:
            errores.append(mensaje)

    return len(errores) == 0, errores


def get_allowed_foods_for_child(db: Session, hijo_id: int) -> list[Alimento]:
    """
    Obtiene lista de alimentos permitidos según restricciones del hijo

    Args:
        db: Sesión de base de datos
        hijo_id: ID del hijo

    Returns:
        Lista de alimentos activos que NO violan restricciones
    """
    # Obtener todos los alimentos activos
    alimentos_activos = db.scalars(
        select(Alimento).where(Alimento.activo == True)
    ).all()

    # Filtrar según restricciones
    alimentos_permitidos = []

    for alimento in alimentos_activos:
        es_permitido, _ = check_food_against_restrictions(db, hijo_id, alimento.id)
        if es_permitido:
            alimentos_permitidos.append(alimento)

    return alimentos_permitidos


def get_restrictions_summary(db: Session, hijo_id: int) -> dict:
    """
    Obtiene resumen de restricciones de un hijo

    Args:
        db: Sesión de base de datos
        hijo_id: ID del hijo

    Returns:
        Dict con resumen de restricciones
    """
    restricciones = get_child_restrictions(db, hijo_id)

    alergias = []
    prohibidos = []

    for rest in restricciones:
        if rest.tipo == "alergia" and rest.alimento_id:
            alimento = db.get(Alimento, rest.alimento_id)
            if alimento:
                alergias.append({
                    "id": rest.id,
                    "alimento_id": alimento.id,
                    "alimento_nombre": alimento.nombre
                })

        elif rest.tipo == "prohibido" and rest.texto:
            prohibidos.append({
                "id": rest.id,
                "texto": rest.texto
            })

    return {
        "total_restricciones": len(restricciones),
        "alergias": alergias,
        "prohibidos": prohibidos,
        "tiene_restricciones": len(restricciones) > 0
    }


# Alias para compatibilidad con código existente
validate_restrictions = check_food_against_restrictions