import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

def debug_menu_creation():
    # 1. Login de admin
    login_data = {
        'username': 'admin@nutribox.com',
        'password': 'admin123'
    }
    
    print('1. Obteniendo token de admin...')
    response = requests.post(f'{BASE_URL}/auth/login', data=login_data)
    if response.status_code != 200:
        print(f'   Error en login: {response.status_code}')
        return
    
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    print('   ✅ Token obtenido')
    
    # 2. Listar alimentos disponibles
    print('2. Obteniendo alimentos disponibles...')
    response = requests.get(f'{BASE_URL}/foods/', headers=headers)
    if response.status_code == 200:
        alimentos = response.json()
        print(f'   ✅ Alimentos encontrados: {len(alimentos)}')
        for alimento in alimentos:
            print(f'      - ID: {alimento["id"]}, Nombre: {alimento["nombre"]}')
    else:
        print(f'   ❌ Error obteniendo alimentos: {response.status_code}')
        return
    
    if not alimentos:
        print('   ❌ No hay alimentos en la base de datos')
        return
    
    # 3. Probar crear menú con IDs correctos
    print('3. Probando crear menú...')
    menu_data = {
        'nombre': 'Menu Saludable Lunes',
        'descripcion': 'Menu equilibrado para empezar la semana',
        'dia_semana': 'Lunes',
        'alimentos': [
            {'alimento_id': alimentos[0]['id'], 'cantidad': 1},
            {'alimento_id': alimentos[1]['id'], 'cantidad': 2}
        ]
    }
    
    print(f'   Usando alimentos: ID {alimentos[0]["id"]} y {alimentos[1]["id"]}')
    response = requests.post(
        f'{BASE_URL}/admin/menus/', 
        headers=headers, 
        json=menu_data
    )
    
    print(f'   Status: {response.status_code}')
    if response.status_code == 201:
        new_menu = response.json()
        print(f'   ✅ Menu creado exitosamente: {new_menu["nombre"]} (ID: {new_menu["id"]})')
    else:
        print(f'   ❌ Error creando menu: {response.text}')

if __name__ == '__main__':
    debug_menu_creation()
