from app.db.database import SessionLocal
from app.db.models.core_models import Usuario, Rol, Membresia

def check_admin_user():
    db = SessionLocal()
    try:
        admin = db.query(Usuario).filter(Usuario.email == "admin@nutribox.com").first()
        if admin:
            print("🔍 DATOS DEL USUARIO ADMIN:")
            print(f"   ID: {admin.id}")
            print(f"   Email: {admin.email}")
            print(f"   Rol: {admin.rol.nombre}")
            print(f"   Membresía: {admin.membresia.tipo}")
            print(f"   Activo: {admin.activo}")
        else:
            print("❌ Usuario admin no encontrado")
            
        # Verificar todas las membresías disponibles
        print("\n📊 MEMBRESÍAS DISPONIBLES:")
        membresias = db.query(Membresia).all()
        for mem in membresias:
            print(f"   - {mem.tipo} (Max direcciones: {mem.max_direcciones})")
            
    finally:
        db.close()

if __name__ == "__main__":
    check_admin_user()
