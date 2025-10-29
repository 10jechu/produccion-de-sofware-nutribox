from app.db.database import Base, engine, SessionLocal
from app.db.models import Rol, Membresia, Usuario
from app.core.security import get_password_hash # <-- IMPORTACIÓN CLAVE

def reset_and_seed_base():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Crear Roles
        admin_rol = Rol(nombre="Admin")
        user_rol = Rol(nombre="Usuario")
        db.add_all([admin_rol, user_rol])
        db.flush()

        # Crear Membresias
        prem_mem = Membresia(tipo="Premium", max_direcciones=3)
        db.add(prem_mem)
        db.flush()

        # Crear Usuario Admin con HASH correcto
        admin_user = Usuario(
            nombre="Admin Test",
            email="admin@nutribox.com",
            hash_password=get_password_hash("admin123"), # <-- LA CONTRASEÑA ES admin123
            rol_id=admin_rol.id,
            membresia_id=prem_mem.id,
            activo=True
        )
        db.add(admin_user)
        db.commit()
        print("BASE DE DATOS REINICIADA Y USUARIO ADMIN (admin@nutribox.com / admin123) CREADO.")
    except Exception as e:
        print(f"Error durante el seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    reset_and_seed_base()
