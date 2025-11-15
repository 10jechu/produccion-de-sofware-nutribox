from app.db.database import Base, engine
from app.db.models import address, alimento, core_models, lunchbox, restriction, menu

print('Creando tablas en la base de datos...')

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

print('Tablas creadas exitosamente!')
print('Tablas creadas:')
for table in Base.metadata.tables.keys():
    print(f'   - {table}')
