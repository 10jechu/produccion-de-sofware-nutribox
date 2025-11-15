import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

def test_menu_creation_fixed():
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
    
    # 2. Crear menú completo con alimentos
    print('2. Creando menú completo...')
    menu_data = {
        'nombre': 'Menu Saludable Lunes',
        'descripcion': 'Menu equilibrado para empezar la semana',
        'dia_semana': 'Lunes',
        'alimentos': [
            {'alimento_id': 1, 'cantidad': 1},  # Manzana
            {'alimento_id': 105, 'cantidad': 2}, # Pan Integral
            {'alimento_id': 107, 'cantidad': 1}  # Jugo de Naranja
        ]
    }
    
    response = requests.post(
        f'{BASE_URL}/admin/menus/', 
        headers=headers, 
        json=menu_data
    )
    
    print(f'   Status: {response.status_code}')
    if response.status_code == 201:
        new_menu = response.json()
        print(f'   ✅ Menu creado exitosamente: {new_menu["nombre"]} (ID: {new_menu["id"]})')
        
        # 3. Verificar detalle del menú creado
        print('3. Verificando detalle del menú...')
        response = requests.get(f'{BASE_URL}/admin/menus/{new_menu["id"]}', headers=headers)
        if response.status_code == 200:
            menu_detail = response.json()
            print(f'   ✅ Menu detail obtenido')
            print(f'   Alimentos en el menú: {len(menu_detail["alimentos"])}')
            for alimento in menu_detail['alimentos']:
                print(f'      - {alimento["nombre"]} x{alimento["cantidad"]}')
            print(f'   Nutrición total: {menu_detail["nutricion_total"]}')
        else:
            print(f'   ❌ Error obteniendo detalle: {response.text}')
            
    else:
        print(f'   ❌ Error creando menu: {response.text}')

if __name__ == '__main__':
    test_menu_creation_fixed()
