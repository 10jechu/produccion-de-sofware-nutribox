# app/crud/menu.py
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, delete as sqlalchemy_delete
from app.db.models.menu import MenuPredeterminado, MenuPredeterminadoItem
from app.db.models.alimento import Alimento
from app.db.schemas.menu import MenuPredeterminadoCreate, MenuPredeterminadoUpdate, MenuItemCreate

# --- CRUD para MenuPredeterminado ---

def get_menu_by_id(db: Session, menu_id: int) -> MenuPredeterminado | None:
    """Obtiene un menú predeterminado por ID, cargando sus items y alimentos."""
    return db.scalars(
        select(MenuPredeterminado)
        .options(selectinload(MenuPredeterminado.items).joinedload(MenuPredeterminadoItem.alimento))
        .where(MenuPredeterminado.id == menu_id)
    ).first()

def get_menu_by_nombre(db: Session, nombre: str) -> MenuPredeterminado | None:
    """Busca un menú por nombre."""
    return db.scalar(select(MenuPredeterminado).where(MenuPredeterminado.nombre == nombre))

def list_menus(db: Session) -> list[MenuPredeterminado]:
    """Lista todos los menús predeterminados con sus items y alimentos."""
    return db.scalars(
        select(MenuPredeterminado)
        .options(selectinload(MenuPredeterminado.items).joinedload(MenuPredeterminadoItem.alimento))
        .order_by(MenuPredeterminado.nombre)
    ).all()

def create_menu(db: Session, payload: MenuPredeterminadoCreate) -> MenuPredeterminado:
    """Crea un nuevo menú predeterminado."""
    if get_menu_by_nombre(db, payload.nombre):
        raise ValueError("Ya existe un menú con este nombre.")

    # Crea el menú base
    menu = MenuPredeterminado(nombre=payload.nombre, descripcion=payload.descripcion)
    db.add(menu)
    db.flush() # Para obtener el ID del menú antes de añadir items

    # Añade los items si se proporcionaron
    if payload.items:
        for item_data in payload.items:
            alimento = db.get(Alimento, item_data.alimento_id)
            if not alimento:
                # Podríamos lanzar error o simplemente ignorar item inválido
                print(f"Advertencia: Alimento ID {item_data.alimento_id} no encontrado al crear menú.")
                continue
            item = MenuPredeterminadoItem(
                menu_id=menu.id,
                alimento_id=item_data.alimento_id,
                cantidad=item_data.cantidad
            )
            db.add(item)

    db.commit()
    db.refresh(menu)
    # Recargar con items para devolver el objeto completo
    return get_menu_by_id(db, menu.id)


def update_menu(db: Session, menu_id: int, payload: MenuPredeterminadoUpdate) -> MenuPredeterminado | None:
    """Actualiza el nombre o descripción de un menú."""
    menu = db.get(MenuPredeterminado, menu_id)
    if not menu:
        return None

    update_data = payload.model_dump(exclude_unset=True)

    # Validar nombre único si se cambia
    if "nombre" in update_data and update_data["nombre"] != menu.nombre:
        existing = get_menu_by_nombre(db, update_data["nombre"])
        if existing:
            raise ValueError("Ya existe otro menú con este nombre.")

    for key, value in update_data.items():
        setattr(menu, key, value)

    db.commit()
    db.refresh(menu)
    return menu

def delete_menu(db: Session, menu_id: int) -> bool:
    """Elimina un menú predeterminado y sus items."""
    menu = db.get(MenuPredeterminado, menu_id)
    if not menu:
        return False
    # Los items se borran en cascada por la configuración de relationship
    db.delete(menu)
    db.commit()
    return True

# --- CRUD para MenuPredeterminadoItem ---

def add_item_to_menu(db: Session, menu_id: int, payload: MenuItemCreate) -> MenuPredeterminadoItem | None:
    """Agrega un alimento a un menú predeterminado."""
    menu = db.get(MenuPredeterminado, menu_id)
    if not menu:
        raise LookupError("Menú no encontrado")
    alimento = db.get(Alimento, payload.alimento_id)
    if not alimento:
        raise ValueError("Alimento no encontrado")

    # Verifica si el item ya existe
    existing = db.scalar(
        select(MenuPredeterminadoItem).where(
            MenuPredeterminadoItem.menu_id == menu_id,
            MenuPredeterminadoItem.alimento_id == payload.alimento_id
        )
    )
    if existing:
        raise ValueError("Este alimento ya está en el menú")

    item = MenuPredeterminadoItem(
        menu_id=menu_id,
        alimento_id=payload.alimento_id,
        cantidad=payload.cantidad
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_item_from_menu(db: Session, menu_id: int, alimento_id: int) -> bool:
    """Quita un alimento de un menú predeterminado."""
    result = db.execute(
        sqlalchemy_delete(MenuPredeterminadoItem).where(
            MenuPredeterminadoItem.menu_id == menu_id,
            MenuPredeterminadoItem.alimento_id == alimento_id
        )
    )
    db.commit()
    return result.rowcount > 0 # Retorna True si se eliminó algo

# --- Funciones de Cálculo ---
def calculate_menu_nutrition(menu: MenuPredeterminado) -> dict:
    """Calcula la nutrición total de un menú."""
    total_kcal = 0
    total_prot = 0
    total_carb = 0
    total_cost = 0
    if menu.items:
        for item in menu.items:
            if item.alimento: # Asegura que el alimento se haya cargado
                total_kcal += (item.alimento.kcal or 0) * item.cantidad
                total_prot += (item.alimento.proteinas or 0) * item.cantidad
                total_carb += (item.alimento.carbos or 0) * item.cantidad
                total_cost += (item.alimento.costo or 0) * item.cantidad
    return {
        "calorias": round(total_kcal, 2),
        "proteinas": round(total_prot, 2),
        "carbohidratos": round(total_carb, 2),
        "costo_total": round(total_cost, 2)
    }