from app.db.database import SessionLocal
from app.db.models.core_models import Usuario, Rol, Membresia
from app.core.security import get_password_hash
from sqlalchemy import select

def get_membership(db: SessionLocal, tipo: str) -> Membresia | None:
    # Asegura que la membresía exista o la crea (Premium tiene 3 direcciones)
    mem = db.scalars(select(Membresia).where(Membresia.tipo == tipo)).first()
    if not mem:
        max_dirs = 3 if tipo == "Premium" else 1
        mem = Membresia(tipo=tipo, max_direcciones=max_dirs)
        db.add(mem)
        db.commit()
        db.refresh(mem)
    return mem

def seed_premium_user():
    db = SessionLocal()
    try:
        # 1. Obtener IDs de Membresía y Rol
        premium_mem = get_membership(db, "Premium")
        user_rol = db.scalars(select(Rol).where(Rol.nombre == "Usuario")).first()
        if not user_rol:
            print("ERROR: Rol 'Usuario' no encontrado. Ejecuta db_reset.py.")
            return
        
        # 2. Crear Usuario Premium
        if not db.scalars(select(Usuario).where(Usuario.email == "premium@nutribox.com")).first():
            premium_user = Usuario(
                nombre="User Premium",
                email="premium@nutribox.com",
                hash_password=get_password_hash("test123"), # Contraseña de prueba estándar
                rol_id=user_rol.id,
                membresia_id=premium_mem.id,
                activo=True
            )
            db.add(premium_user)
            db.commit()
            print("INFO: Usuario Premium creado con éxito.")
        else:
            print("INFO: Usuario Premium ya existe.")
        
    except Exception as e:
        print(f"ERROR durante la creación del usuario Premium: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    seed_premium_user()
