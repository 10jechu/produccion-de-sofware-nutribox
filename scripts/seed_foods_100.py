from app.db.database import SessionLocal
from app.db.models import Alimento
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

def get_base_foods():
    # 20 Alimentos base con EMOJIS, categorías y precios estimados en COP
    return [
        # --- 1. FRUTAS (Baja Caloría) ---
        {"nombre": "🍎 Manzana Roja", "kcal": 55.0, "proteinas": 0.3, "carbos": 14.0, "costo": 1800.0},
        {"nombre": "🍌 Bananito (Unidad)", "kcal": 90.0, "proteinas": 1.1, "carbos": 23.0, "costo": 800.0},
        {"nombre": "🍊 Gajos de Mandarina", "kcal": 40.0, "proteinas": 0.6, "carbos": 10.0, "costo": 1200.0},
        {"nombre": "🍐 Pera Nacional", "kcal": 60.0, "proteinas": 0.4, "carbos": 15.0, "costo": 1800.0},
        
        # --- 2. VERDURAS (Muy Baja Caloría) ---
        {"nombre": "🥕 Zanahoria Baby", "kcal": 25.0, "proteinas": 0.5, "carbos": 6.0, "costo": 2000.0},
        {"nombre": "🍅 Tomate Cherry (5u)", "kcal": 15.0, "proteinas": 0.8, "carbos": 3.0, "costo": 1000.0},
        
        # --- 3. PROTEÍNA ALTA (Lácteos/Animal) ---
        {"nombre": "🥚 Huevo Duro (Unidad)", "kcal": 78.0, "proteinas": 6.3, "carbos": 0.6, "costo": 700.0},
        {"nombre": "🥛 Yogurt Griego (100g)", "kcal": 80.0, "proteinas": 10.0, "carbos": 4.0, "costo": 3500.0},
        {"nombre": "🧀 Queso Mozzarella (30g)", "kcal": 90.0, "proteinas": 7.0, "carbos": 1.0, "costo": 1500.0},
        {"nombre": "🍗 Pollo Desmenuzado (30g)", "kcal": 50.0, "proteinas": 9.0, "carbos": 0.0, "costo": 2500.0},
        
        # --- 4. SNACKS SALUDABLES/GRANOS ---
        {"nombre": "🍪 Galletas Integrales (2u)", "kcal": 120.0, "proteinas": 2.5, "carbos": 20.0, "costo": 1100.0},
        {"nombre": "🌾 Barra de Cereal Integral", "kcal": 110.0, "proteinas": 2.0, "carbos": 20.0, "costo": 1600.0},
        {"nombre": "🌰 Mix de Frutos Secos (15g)", "kcal": 95.0, "proteinas": 3.0, "carbos": 3.0, "costo": 3000.0},
        {"nombre": "🍞 Arepa Pequeña", "kcal": 150.0, "proteinas": 3.0, "carbos": 32.0, "costo": 500.0},

        # --- 5. BEBIDAS Y DIVERSOS ---
        {"nombre": "💧 Agua (Botella 300ml)", "kcal": 0.0, "proteinas": 0.0, "carbos": 0.0, "costo": 1000.0},
        {"nombre": "🥤 Jugo de Naranja Natural (200ml)", "kcal": 85.0, "proteinas": 0.5, "carbos": 20.0, "costo": 2200.0},
        {"nombre": "🥖 Pan con Avena (1u)", "kcal": 80.0, "proteinas": 4.0, "carbos": 15.0, "costo": 400.0},
        {"nombre": "🥣 Gelatina sin Azúcar", "kcal": 10.0, "proteinas": 1.0, "carbos": 1.0, "costo": 800.0},
        {"nombre": "🍘 Tostadas Integrales (2u)", "kcal": 110.0, "proteinas": 3.0, "carbos": 22.0, "costo": 1500.0},
        {"nombre": "🧀 Queso Pera", "kcal": 120.0, "proteinas": 8.0, "carbos": 2.0, "costo": 2000.0},
    ]

def seed_foods_100():
    db = SessionLocal()
    clear_foods_table(db)
    
    foods_to_insert = []
    base_foods = get_base_foods()
    
    # Bucle para insertar 5 copias de los 20 ítems, total 100.
    for i in range(5):
        for food_data in base_foods:
            # Crea una copia y actualiza la clave 'nombre'
            temp_food_data = food_data.copy()
            new_name = f"{temp_food_data['nombre']} V{i+1}"
            temp_food_data['nombre'] = new_name 
            
            alimento = Alimento(**temp_food_data)
            foods_to_insert.append(alimento)

    try:
        db.add_all(foods_to_insert)
        db.commit()
        print(f"INFO: Se agregaron {len(foods_to_insert)} alimentos de prueba a la base de datos.")
    except Exception as e:
        print(f"ERROR: No se pudieron insertar todos los alimentos. {e}")
        db.rollback()
    finally:
        db.close()

def clear_foods_table(db: Session):
    db.execute(delete(Alimento))
    db.commit()
    print("INFO: Tabla de Alimentos limpiada.")

if __name__ == '__main__':
    seed_foods_100()
