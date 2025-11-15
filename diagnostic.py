import sys
import os

print('DIAGNOSTICO DEL SISTEMA NUTRIBOX')

# Verificar estructura de archivos
required_files = [
    'app/db/models/menu.py',
    'app/db/schemas/menu.py', 
    'app/crud/menu.py',
    'app/api/v1/routers/admin_menus.py',
    'app/api/v1/routers/routes.py'
]

print('VERIFICANDO ARCHIVOS CREADOS:')
all_exist = True
for file_path in required_files:
    if os.path.exists(file_path):
        print(f'   OK - {file_path}')
    else:
        print(f'   ERROR - {file_path} - NO EXISTE')
        all_exist = False

# Verificar imports
print('VERIFICANDO IMPORTS...')
try:
    from app.db.models.menu import Menu
    from app.db.schemas.menu import MenuCreate
    from app.crud.menu import create_menu
    from app.api.v1.routers.admin_menus import router
    print('   OK - Todos los imports funcionan correctamente')
except ImportError as e:
    print(f'   ERROR en imports: {e}')
    all_exist = False

# Verificar base de datos
print('VERIFICANDO BASE DE DATOS...')
try:
    from app.db.database import engine
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    required_tables = ['menus', 'menu_alimento']
    for table in required_tables:
        if table in tables:
            print(f'   OK - Tabla {table} existe')
        else:
            print(f'   ERROR - Tabla {table} NO existe')
            all_exist = False
            
except Exception as e:
    print(f'   ERROR verificando BD: {e}')
    all_exist = False

print(f'RESUMEN: TODO CORRECTO' if all_exist else 'RESUMEN: HAY PROBLEMAS')

if not all_exist:
    print('Algunos archivos/tablas no se crearon correctamente.')
    print('Revisa los mensajes anteriores y ejecuta los scripts nuevamente.')
else:
    print('Sistema listo! Puedes continuar con los siguientes endpoints.')
