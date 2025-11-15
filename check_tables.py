from app.db.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()

print('TABLAS EN LA BASE DE DATOS:')
for table in tables:
    print(f'   {table}')
    
# Verificar tablas críticas
critical_tables = ['menus', 'menu_alimento', 'alimentos', 'usuarios', 'hijos', 'loncheras']
print('VERIFICACION DE TABLAS CRITICAS:')
for table in critical_tables:
    if table in tables:
        print(f'   {table} - EXISTE')
    else:
        print(f'   {table} - NO EXISTE')
