from app.db.database import SessionLocal
from app.db.models.core_models import Usuario, Rol, Membresia
from app.core.security import get_password_hash
from sqlalchemy import select

def get_membership(db: SessionLocal, tipo: str) -> Membresia | None:
    # Intenta buscar la membresía existente o la crea si no existe (Failsafe)
    mem = db.scalars(select(Membresia).where(Membresia.tipo == tipo)).first()
    if not mem:
        max_dirs = 3 if tipo == "Premium" else 1
        mem = Membresia(tipo=tipo, max_direcciones=max_dirs)
        db.add(mem)
        db.commit()
        db.refresh(mem)
    return mem

def seed_test_users():
    db = SessionLocal()
    try:
        # 1. Obtener IDs de Membresía (Aseguramos su existencia)
        free_mem = get_membership(db, "Free")
        estandar_mem = get_membership(db, "Estandar")
        
        # 2. Obtener ID de Rol (Asumimos 'Usuario')
        user_rol = db.scalars(select(Rol).where(Rol.nombre == "Usuario")).first()
        if not user_rol:
            print("ERROR: Rol 'Usuario' no encontrado. Ejecuta db_reset.py.")
            return
        
        # 3. Crear Usuario Estándar
        if not db.scalars(select(Usuario).where(Usuario.email == "estandar@nutribox.com")).first():
            estandar_user = Usuario(
                nombre="User Estandar",
                email="estandar@nutribox.com",
                hash_password=get_password_hash("test123"),
                rol_id=user_rol.id,
                membresia_id=estandar_mem.id,
                activo=True
            )
            db.add(estandar_user)

        # 4. Crear Usuario Básico (Gratis)
        if not db.scalars(select(Usuario).where(Usuario.email == "gratis@nutribox.com")).first():
            free_user = Usuario(
                nombre="User Gratis",
                email="gratis@nutribox.com",
                hash_password=get_password_hash("test123"),
                rol_id=user_rol.id,
                membresia_id=free_mem.id,
                activo=True
            )
            db.add(free_user)
        
        db.commit()
        print("INFO: Usuarios de Prueba (Estándar/Gratis) creados con contraseña 'test123'.")
        
    except Exception as e:
        print(f"ERROR durante el seeding de usuarios de prueba: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    seed_test_users()
