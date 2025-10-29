from app.db.database import SessionLocal
from app.db.models.core_models import Rol, Usuario

def assign_admin():
    db = SessionLocal()
    try:
        # Asegurar Rol 'Admin'
        admin_role = db.query(Rol).filter_by(nombre="Admin").first()
        if not admin_role:
            admin_role = Rol(nombre="Admin")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
        
        # Asignar rol Admin al usuario demo (demo@nutribox.com)
        demo_user = db.query(Usuario).filter_by(email="demo@nutribox.com").first()
        if demo_user:
            demo_user.rol_id = admin_role.id
            db.commit()
            print("INFO: Rol Admin asignado a demo@nutribox.com")
        else:
            print("ADVERTENCIA: Usuario demo no encontrado. Ejecuta 'POST /dev/seed' en Swagger y vuelve a ejecutar este script.")

    finally:
        db.close()

if __name__ == '__main__':
    assign_admin()
