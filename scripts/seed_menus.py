from app.db.database import SessionLocal
from app.db.models import Lonchera, LoncheraAlimento, Usuario, Hijo # Importar Hijo
from app.crud.alimento import list_ as list_foods
from datetime import date
from sqlalchemy import delete as sqlalchemy_delete, select

# ID del usuario Administrador (para crear los menús base)
ADMIN_USER_ID = 1

def seed_menus():
    db = SessionLocal()
    
    # 1. Obtener alimentos (ya deben tener emojis y datos)
    foods_map = {f.nombre: f for f in list_foods(db, only_active=True)}
    
    # 2. Definir Menús (Alta proteína / Saludables)
    menus_data = [
        {
            "nombre": "💪 Menú Power Proteína",
            "descripcion": "Lonchera alta en proteínas para energía sostenida. Ideal para la mañana.",
            "items": [
                {"alimento": "🥚 Huevo Duro (Unidad) V1", "cantidad": 2},
                {"alimento": "🍎 Manzana Roja V1", "cantidad": 1},
                {"alimento": "🥛 Yogurt Griego (100g) V1", "cantidad": 1},
            ]
        },
        {
            "nombre": "💚 Menú Veggie Fresh",
            "descripcion": "Opción baja en calorías y rica en fibra. Perfecto para la tarde.",
            "items": [
                {"alimento": "🥕 Zanahoria Baby V1", "cantidad": 1},
                {"alimento": "🧀 Queso Mozzarella (30g) V1", "cantidad": 1},
                {"alimento": "🌰 Mix de Frutos Secos (15g) V1", "cantidad": 1},
                {"alimento": "💧 Agua (Botella 300ml) V1", "cantidad": 1},
            ]
        },
        {
            "nombre": "⚡ Menú Carbo Equilibrado",
            "descripcion": "Balance entre carbohidratos complejos y proteína. Para días de deporte.",
            "items": [
                {"alimento": "🍞 Arepa Pequeña V1", "cantidad": 1},
                {"alimento": "🍗 Pollo Desmenuzado (30g) V1", "cantidad": 1},
                {"alimento": "🍌 Bananito (Unidad) V1", "cantidad": 1},
            ]
        },
        {
            "nombre": "🥛 Menú Lácteo Suave",
            "descripcion": "Ideal para niños pequeños. Rica en calcio y fácil de digerir.",
            "items": [
                {"alimento": "🥛 Yogurt Griego (100g) V2", "cantidad": 1},
                {"alimento": "🍪 Galletas Integrales (2u) V1", "cantidad": 1},
                {"alimento": "🍊 Gajos de Mandarina V1", "cantidad": 1},
            ]
        },
        {
            "nombre": "🍽️ Menú Diversidad",
            "descripcion": "Una mezcla de todo. Opción por defecto para dietas variadas.",
            "items": [
                {"alimento": "🥚 Huevo Duro (Unidad) V2", "cantidad": 1},
                {"alimento": "🌾 Barra de Cereal Integral V1", "cantidad": 1},
                {"alimento": "🥤 Jugo de Naranja Natural (200ml) V1", "cantidad": 1},
            ]
        },
    ]

    try:
        # CORRECCIÓN DE CONSULTA CRÍTICA: Buscar el hijo directamente por el usuario_id
        admin_hijo = db.scalars(select(Hijo).where(Hijo.usuario_id == ADMIN_USER_ID)).first()
        
        if admin_hijo:
            # 3. Limpiar menús anteriores (usando el ID del hijo encontrado)
            db.execute(sqlalchemy_delete(LoncheraAlimento).where(LoncheraAlimento.lonchera_id.in_(
                db.scalars(select(Lonchera.id).where(Lonchera.hijo_id == admin_hijo.id)).all()
            )))
            db.execute(sqlalchemy_delete(Lonchera).where(Lonchera.hijo_id == admin_hijo.id))
            db.commit()
            print("INFO: Loncheras/Menús de Admin limpiados.")
        else:
            print("ADVERTENCIA: Admin no tiene hijos. Ejecuta el script de creación de hijo y luego reinicia.")
            return

        # 4. Insertar los nuevos menús
        for menu_data in menus_data:
            # 1. Crear la Lonchera (Menu)
            lonchera = Lonchera(
                hijo_id=admin_hijo.id,
                fecha=date.today(),
                estado=menu_data["nombre"],
                direccion_id=None
            )
            db.add(lonchera)
            db.flush()

            # 2. Agregar los items
            for item in menu_data["items"]:
                alimento_obj = foods_map.get(item["alimento"])
                if alimento_obj:
                    lonchera_item = LoncheraAlimento(
                        lonchera_id=lonchera.id,
                        alimento_id=alimento_obj.id,
                        cantidad=item["cantidad"]
                    )
                    db.add(lonchera_item)
                else:
                    print(f"ERROR: Alimento '{item['alimento']}' no encontrado. Saltando ítem.")
        
        db.commit()
        print(f"INFO: Se crearon {len(menus_data)} Menús Predeterminados.")

    except Exception as e:
        print(f"ERROR en seeding de menús: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    seed_menus()
