from app.core.config import settings

print("🔧 VERIFICANDO CONFIGURACIÓN:")
print(f"✅ DATABASE_URL: {settings.DATABASE_URL}")
print(f"✅ SECRET_KEY: {settings.SECRET_KEY}")
print(f"✅ ALGORITHM: {settings.ALGORITHM}")
print(f"✅ APP_NAME: {settings.app_name}")

# Probar la conexión a la base de datos
try:
    from app.db.database import engine
    print("✅ Base de datos configurada correctamente")
except Exception as e:
    print(f"❌ Error en base de datos: {e}")
