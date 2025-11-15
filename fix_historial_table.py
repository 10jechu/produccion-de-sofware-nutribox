from app.db.database import engine, Base
from app.db.models.historial import HistorialAlimento

print("🗃️ Recreando tabla historial_alimentos...")

# Eliminar tabla si existe
Base.metadata.drop_all(bind=engine, tables=[HistorialAlimento.__table__])

# Crear tabla con la estructura correcta
Base.metadata.create_all(bind=engine, tables=[HistorialAlimento.__table__])

print("✅ Tabla historial_alimentos recreada correctamente")
