import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

def test_admin_menus():
    'Probar endpoints de menus admin'
    
    # Primero necesitamos login de admin
    login_data = {
        'username': 'admin@nutribox.com',  # Ajustar según tus datos
        'password': 'admin123'
    }
    
    print('Obteniendo token de admin...')
    try:
        response = requests.post(f'{BASE_URL}/auth/login', data=login_data)
        if response.status_code != 200:
            print(f'Login fallo: {response.status_code}')
            return None
        
        token = response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print('Token obtenido exitosamente')
        
        # 1. Listar menus
        print('Probando GET /admin/menus...')
        response = requests.get(f'{BASE_URL}/admin/menus/', headers=headers)
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            menus = response.json()
            print(f'Menus encontrados: {len(menus)}')
        else:
            print(f'Error: {response.text}')
        
        # 2. Crear menu de prueba
        print('Probando POST /admin/menus...')
        menu_data = {
            'nombre': 'Menu Saludable Lunes',
            'descripcion': 'Menu equilibrado para empezar la semana',
            'dia_semana': 'Lunes',
            'alimentos': [
                {'alimento_id': 1, 'cantidad': 1},  # Ajustar IDs según tu BD
                {'alimento_id': 2, 'cantidad': 2}
            ]
        }
        
        response = requests.post(
            f'{BASE_URL}/admin/menus/', 
            headers=headers, 
            json=menu_data
        )
        print(f'Status: {response.status_code}')
        if response.status_code == 201:
            new_menu = response.json()
            print(f'Menu creado: {new_menu['nombre']} (ID: {new_menu['id']})')
            return new_menu['id']
        else:
            print(f'Error creando menu: {response.text}')
            return None
            
    except Exception as e:
        print(f'Error en prueba: {e}')
        return None

def test_regular_user_menus():
    'Probar que usuario regular NO puede acceder a admin menus'
    
    # Login de usuario regular
    login_data = {
        'username': 'usuario@ejemplo.com',  # Ajustar según tus datos
        'password': 'password123'
    }
    
    print('Probando acceso de usuario regular...')
    try:
        response = requests.post(f'{BASE_URL}/auth/login', data=login_data)
        if response.status_code != 200:
            print('Login de usuario fallo')
            return
        
        token = response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Intentar acceder a admin menus
        response = requests.get(f'{BASE_URL}/admin/menus/', headers=headers)
        print(f'Status esperado 403, obtenido: {response.status_code}')
        if response.status_code == 403:
            print('Correcto: Usuario regular no puede acceder a admin menus')
        else:
            print('Problema: Usuario regular pudo acceder')
            
    except Exception as e:
        print(f'Error en prueba usuario: {e}')

if __name__ == '__main__':
    print('INICIANDO PRUEBAS DE ENDPOINTS MENU ADMIN')
    
    # Probar admin
    menu_id = test_admin_menus()
    
    # Probar usuario regular
    test_regular_user_menus()
    
    print('PRUEBAS COMPLETADAS')
