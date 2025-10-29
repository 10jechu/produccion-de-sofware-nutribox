from app.db.database import SessionLocal
from app.db.models import Hijo
from app.db.models.core_models import Usuario
from sqlalchemy import select

# El Admin se crea con ID 1 en db_reset.py
ADMIN_USER_EMAIL = "admin@nutribox.com" 

def create_admin_child():
    db = SessionLocal()
    try:
        admin_user = db.scalars(select(Usuario).where(Usuario.email == ADMIN_USER_EMAIL)).first()
        if not admin_user:
            print("ERROR: Usuario Admin no encontrado. Ejecuta db_reset.py primero.")
            return

        # Verificar si el hijo ya existe
        if db.scalars(select(Hijo).where(Hijo.usuario_id == admin_user.id)).first():
            print("INFO: El hijo del Administrador ya existe.")
            return

        hijo = Hijo(nombre="Admin\'s Menu-Child", usuario_id=admin_user.id)
        db.add(hijo)
        db.commit()
        print(f"INFO: Hijo del Administrador ('{hijo.nombre}') creado con ID {hijo.id}.")

    except Exception as e:
        print(f"ERROR creando hijo: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    create_admin_child()
