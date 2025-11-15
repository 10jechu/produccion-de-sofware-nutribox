from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.models.menu import Menu, menu_alimento
from app.db.models.alimento import Alimento
from app.db.models.core_models import Usuario

def list_menus(db: Session, activo_only: bool = True) -> list[Menu]:
    "Lista todos los menus (solo activos por defecto)"
    stmt = select(Menu)
    if activo_only:
        stmt = stmt.where(Menu.activo == True)
    return db.scalars(stmt).all()

def get_menu_by_id(db: Session, menu_id: int) -> Menu | None:
    "Obtiene un menu por ID"
    return db.get(Menu, menu_id)

def create_menu(db: Session, payload, usuario_id: int) -> Menu:
    "Crea un nuevo menu predeterminado"
    try:
        # Verificar que el usuario existe
        usuario = db.get(Usuario, usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        # Crear el menu
        menu_data = payload.model_dump(exclude={"alimentos"})
        menu = Menu(**menu_data, usuario_id=usuario_id)
        db.add(menu)
        db.commit()  # Commit primero para obtener ID
        db.refresh(menu)
        
        # Agregar alimentos al menu si existen
        if hasattr(payload, 'alimentos') and payload.alimentos:
            for item in payload.alimentos:
                alimento = db.get(Alimento, item.alimento_id)
                if not alimento:
                    raise ValueError(f"Alimento con ID {item.alimento_id} no encontrado")
                
                # Insertar en tabla de asociación
                insert_stmt = menu_alimento.insert().values(
                    menu_id=menu.id,
                    alimento_id=item.alimento_id,
                    cantidad=item.cantidad
                )
                db.execute(insert_stmt)
            
            db.commit()
            db.refresh(menu)
        
        return menu
        
    except Exception as e:
        db.rollback()
        raise e

def update_menu(db: Session, menu_id: int, payload) -> Menu:
    "Actualiza un menu existente"
    menu = db.get(Menu, menu_id)
    if not menu:
        raise LookupError("Menu no encontrado")
    
    data = payload.model_dump(exclude_unset=True, exclude={"alimentos"})
    for key, value in data.items():
        setattr(menu, key, value)
    
    db.commit()
    db.refresh(menu)
    return menu

def delete_menu(db: Session, menu_id: int) -> None:
    "Elimina un menu (soft delete)"
    menu = db.get(Menu, menu_id)
    if not menu:
        raise LookupError("Menu no encontrado")
    
    menu.activo = False
    db.commit()

def get_menu_with_alimentos_formatted(db: Session, menu_id: int) -> dict:
    "Obtiene menu con alimentos formateados para el esquema"
    menu = db.get(Menu, menu_id)
    if not menu:
        return None
    
    # Obtener alimentos con cantidad usando la relación existente
    alimentos_data = db.execute(
        select(
            Alimento.id,
            Alimento.nombre,
            Alimento.kcal,
            Alimento.proteinas,
            Alimento.carbos,
            menu_alimento.c.cantidad
        )
        .select_from(menu_alimento)
        .join(Alimento, Alimento.id == menu_alimento.c.alimento_id)
        .where(menu_alimento.c.menu_id == menu_id)
    ).all()
    
    # Formatear para el esquema
    alimentos_formateados = [
        {
            "alimento_id": item.id,
            "nombre": item.nombre,
            "cantidad": item.cantidad,
            "kcal": item.kcal,
            "proteinas": item.proteinas,
            "carbos": item.carbos
        }
        for item in alimentos_data
    ]
    
    return {
        "id": menu.id,
        "nombre": menu.nombre,
        "descripcion": menu.descripcion,
        "dia_semana": menu.dia_semana,
        "activo": menu.activo,
        "usuario_id": menu.usuario_id,
        "alimentos": alimentos_formateados
    }

def get_menu_detail(db: Session, menu_id: int) -> dict:
    "Obtiene detalle completo del menu con nutrición"
    menu = db.get(Menu, menu_id)
    if not menu:
        return None
    
    # Obtener alimentos del menu con información nutricional
    alimentos_data = db.execute(
        select(
            Alimento.id,
            Alimento.nombre,
            Alimento.kcal,
            Alimento.proteinas,
            Alimento.carbos,
            menu_alimento.c.cantidad
        )
        .select_from(menu_alimento)
        .join(Alimento, Alimento.id == menu_alimento.c.alimento_id)
        .where(menu_alimento.c.menu_id == menu_id)
    ).all()
    
    # Calcular nutrición total
    total_cal = sum(item.kcal * item.cantidad for item in alimentos_data)
    total_prot = sum(item.proteinas * item.cantidad for item in alimentos_data)
    total_carb = sum(item.carbos * item.cantidad for item in alimentos_data)
    
    alimentos_list = [
        {
            "alimento_id": item.id,
            "nombre": item.nombre,
            "cantidad": item.cantidad,
            "kcal": item.kcal,
            "proteinas": item.proteinas,
            "carbos": item.carbos
        }
        for item in alimentos_data
    ]
    
    return {
        "id": menu.id,
        "nombre": menu.nombre,
        "descripcion": menu.descripcion,
        "dia_semana": menu.dia_semana,
        "activo": menu.activo,
        "usuario_id": menu.usuario_id,
        "creador_nombre": menu.creador.nombre,
        "alimentos": alimentos_list,
        "nutricion_total": {
            "calorias": round(total_cal, 2),
            "proteinas": round(total_prot, 2),
            "carbohidratos": round(total_carb, 2)
        }
    }
