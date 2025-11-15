import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

def debug_error_500():
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
    
    # 2. Probar con datos más simples
    print('2. Probando con datos mínimos...')
    menu_data_simple = {
        'nombre': 'Menu Test Simple',
        'descripcion': 'Menu de prueba simple',
        'dia_semana': 'Lunes',
        'alimentos': []  # Sin alimentos primero
    }
    
    response = requests.post(
        f'{BASE_URL}/admin/menus/', 
        headers=headers, 
        json=menu_data_simple
    )
    
    print(f'   Status (sin alimentos): {response.status_code}')
    if response.status_code == 201:
        print('   ✅ Menu creado sin alimentos')
        menu_id = response.json()['id']
    else:
        print(f'   ❌ Error: {response.text}')
        return
    
    # 3. Probar agregar alimentos después
    print('3. Probando agregar alimentos...')
    # Primero verificar el endpoint de detalle
    response = requests.get(f'{BASE_URL}/admin/menus/{menu_id}', headers=headers)
    print(f'   GET Menu Detail Status: {response.status_code}')
    if response.status_code == 200:
        print('   ✅ Menu detail funciona')
    else:
        print(f'   ❌ Menu detail error: {response.text}')

if __name__ == '__main__':
    debug_error_500()
