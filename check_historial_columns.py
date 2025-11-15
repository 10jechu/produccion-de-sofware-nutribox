from sqlalchemy import inspect
from app.db.database import engine

inspector = inspect(engine)
columns = inspector.get_columns('historial_alimentos')

print("📋 COLUMNAS DE HISTORIAL_ALIMENTOS:")
for column in columns:
    print(f"   - {column['name']} ({column['type']})")
