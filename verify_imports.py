print("🔧 VERIFICANDO IMPORTACIONES...")

modules_to_check = [
    "app.core.security",
    "app.core.security_deps", 
    "app.core.deps",
    "app.core.config",
    "app.db.database",
    "app.api.v1.routers.auth"
]

for module_name in modules_to_check:
    try:
        __import__(module_name)
        print(f"✅ {module_name}")
    except ImportError as e:
        print(f"❌ {module_name}: {e}")

print("\n🔍 VERIFICANDO FUNCIONES ESPECÍFICAS...")
try:
    from app.core.security import verify_token, decode_token, create_access_token
    print("✅ Todas las funciones de seguridad importan correctamente")
except ImportError as e:
    print(f"❌ Error en funciones de seguridad: {e}")

try:
    from app.core.deps import get_db, decode_token
    print("✅ Funciones de dependencias importan correctamente")
except ImportError as e:
    print(f"❌ Error en dependencias: {e}")
