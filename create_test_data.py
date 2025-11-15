from app.db.database import SessionLocal
from app.db.models.core_models import Usuario, Rol, Membresia
from app.db.models.alimento import Alimento
from app.core.security import get_password_hash

def create_test_data():
    db = SessionLocal()
    try:
        print("Creando datos de prueba...")
        
        # Crear rol de admin si no existe
        admin_rol = db.query(Rol).filter_by(nombre="Admin").first()
        if not admin_rol:
            admin_rol = Rol(nombre="Admin")
            db.add(admin_rol)
            db.commit()
            db.refresh(admin_rol)
            print("Rol Admin creado")
        
        # Crear membresías si no existen
        membresias_data = [
            {"tipo": "Free", "max_direcciones": 0},
            {"tipo": "Estandar", "max_direcciones": 1},
            {"tipo": "Premium", "max_direcciones": 3}
        ]
        
        for mem_data in membresias_data:
            if not db.query(Membresia).filter_by(tipo=mem_data["tipo"]).first():
                membresia = Membresia(**mem_data)
                db.add(membresia)
                print(f"Membresia {mem_data['tipo']} creada")
        
        db.commit()
        
        # Crear usuario admin si no existe
        admin_user = db.query(Usuario).filter_by(email="admin@nutribox.com").first()
        if not admin_user:
            premium_membresia = db.query(Membresia).filter_by(tipo="Premium").first()
            admin_user = Usuario(
                nombre="Administrador",
                email="admin@nutribox.com",
                hash_password=get_password_hash("admin123"),
                rol_id=admin_rol.id,
                membresia_id=premium_membresia.id,
                activo=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("Usuario admin creado: admin@nutribox.com / admin123")
        
        # Crear algunos alimentos de prueba
        alimentos_data = [
            {"nombre": "Manzana", "kcal": 52, "proteinas": 0.3, "carbos": 14, "costo": 1.5},
            {"nombre": "Pan Integral", "kcal": 265, "proteinas": 9, "carbos": 49, "costo": 2.0},
            {"nombre": "Queso", "kcal": 402, "proteinas": 25, "carbos": 2, "costo": 3.5},
            {"nombre": "Jugo de Naranja", "kcal": 45, "proteinas": 0.7, "carbos": 10, "costo": 2.5},
        ]
        
        for alimento_data in alimentos_data:
            if not db.query(Alimento).filter_by(nombre=alimento_data["nombre"]).first():
                alimento = Alimento(**alimento_data)
                db.add(alimento)
                print(f"Alimento {alimento_data['nombre']} creado")
        
        db.commit()
        print("Datos de prueba creados exitosamente!")
        
    except Exception as e:
        print(f"Error creando datos de prueba: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
