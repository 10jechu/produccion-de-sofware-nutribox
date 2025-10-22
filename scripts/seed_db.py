"""Script para poblar la base de datos con datos iniciales"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.models import Base
from app.db.models.core_models import Rol, Membresia, Usuario
from app.db.models.alimento import Alimento
from app.core.security import get_password_hash

def seed_database():
    # Crear todas las tablas
    print("� Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("� Iniciando seed de base de datos...")
        
        # 1. Roles
        print("� Creando roles...")
        roles = ["Admin", "Usuario"]
        for rol_nombre in roles:
            if not db.query(Rol).filter_by(nombre=rol_nombre).first():
                rol = Rol(nombre=rol_nombre)
                db.add(rol)
        db.commit()
        print("✅ Roles creados")
        
        # 2. Membresías
        print("� Creando membresías...")
        membresias_data = [
            {"tipo": "Free", "max_direcciones": 1, "descripcion": "Plan gratuito básico"},
            {"tipo": "Premium", "max_direcciones": 3, "descripcion": "Plan premium con todas las funcionalidades"}
        ]
        for mem_data in membresias_data:
            if not db.query(Membresia).filter_by(tipo=mem_data["tipo"]).first():
                membresia = Membresia(**mem_data)
                db.add(membresia)
        db.commit()
        print("✅ Membresías creadas")
        
        # 3. Usuario administrador
        print("� Creando usuario administrador...")
        admin_rol = db.query(Rol).filter_by(nombre="Admin").first()
        premium_mem = db.query(Membresia).filter_by(tipo="Premium").first()
        
        if not db.query(Usuario).filter_by(email="admin@nutribox.com").first():
            admin = Usuario(
                nombre="Administrador",
                email="admin@nutribox.com",
                hash_password=get_password_hash("Admin123!"),
                rol_id=admin_rol.id,
                membresia_id=premium_mem.id,
                activo=True
            )
            db.add(admin)
            db.commit()
            print("✅ Admin creado: admin@nutribox.com / Admin123!")
        else:
            print("ℹ️  Admin ya existe")
        
        # 4. Alimentos de ejemplo
        print("� Creando alimentos de ejemplo...")
        alimentos_data = [
            {"nombre": "Manzana", "descripcion": "Fruta fresca rica en fibra", "calorias": 52, "proteinas": 0.3, "grasas": 0.2, "carbohidratos": 14},
            {"nombre": "Banana", "descripcion": "Fuente de potasio", "calorias": 89, "proteinas": 1.1, "grasas": 0.3, "carbohidratos": 23},
            {"nombre": "Sandwich de jamón", "descripcion": "Pan integral con jamón de pavo", "calorias": 250, "proteinas": 15, "grasas": 8, "carbohidratos": 30},
            {"nombre": "Yogurt natural", "descripcion": "Yogurt sin azúcar añadida", "calorias": 60, "proteinas": 5, "grasas": 3, "carbohidratos": 7},
            {"nombre": "Galletas integrales", "descripcion": "Paquete de 5 galletas", "calorias": 120, "proteinas": 2, "grasas": 4, "carbohidratos": 20},
            {"nombre": "Jugo de naranja natural", "descripcion": "200ml de jugo recién exprimido", "calorias": 90, "proteinas": 1, "grasas": 0, "carbohidratos": 21},
            {"nombre": "Zanahoria baby", "descripcion": "Zanahorias pequeñas crudas", "calorias": 35, "proteinas": 0.8, "grasas": 0.2, "carbohidratos": 8},
            {"nombre": "Queso fresco", "descripcion": "Porción de 30g", "calorias": 80, "proteinas": 6, "grasas": 6, "carbohidratos": 1},
        ]
        
        for alimento_data in alimentos_data:
            if not db.query(Alimento).filter_by(nombre=alimento_data["nombre"]).first():
                alimento = Alimento(**alimento_data)
                db.add(alimento)
        db.commit()
        print("✅ Alimentos creados")
        
        print("\n" + "="*50)
        print("� Seed completado exitosamente!")
        print("="*50)
        print("\n� Credenciales de admin:")
        print("   Email: admin@nutribox.com")
        print("   Password: Admin123!")
        print("\n� Datos creados:")
        print(f"   - Roles: {db.query(Rol).count()}")
        print(f"   - Membresías: {db.query(Membresia).count()}")
        print(f"   - Usuarios: {db.query(Usuario).count()}")
        print(f"   - Alimentos: {db.query(Alimento).count()}")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"❌ Error durante el seed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
