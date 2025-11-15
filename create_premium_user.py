from app.db.database import SessionLocal
from app.db.models.core_models import Usuario, Rol, Membresia
from app.core.security import get_password_hash

def create_premium_test_user():
    db = SessionLocal()
    try:
        # Buscar rol de usuario normal
        rol_usuario = db.query(Rol).filter(Rol.nombre == "Usuario").first()
        if not rol_usuario:
            rol_usuario = Rol(nombre="Usuario")
            db.add(rol_usuario)
            db.commit()
            print("✅ Rol Usuario creado")
        
        # Buscar membresía Premium
        membresia_premium = db.query(Membresia).filter(Membresia.tipo == "Premium").first()
        if not membresia_premium:
            print("❌ Membresía Premium no encontrada")
            return
        
        # Crear usuario premium de prueba
        premium_user = db.query(Usuario).filter(Usuario.email == "premium@test.com").first()
        if not premium_user:
            premium_user = Usuario(
                nombre="Usuario Premium Test",
                email="premium@test.com",
                hash_password=get_password_hash("premium123"),
                rol_id=rol_usuario.id,
                membresia_id=membresia_premium.id,
                activo=True
            )
            db.add(premium_user)
            db.commit()
            db.refresh(premium_user)
            print("✅ Usuario Premium creado:")
            print(f"   Email: premium@test.com")
            print(f"   Password: premium123")
            print(f"   Membresía: {premium_user.membresia.tipo}")
        else:
            print("✅ Usuario Premium ya existe")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_premium_test_user()
