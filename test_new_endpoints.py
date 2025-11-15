import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

def test_new_endpoints():
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
    
    # 2. Probar endpoint consolidado hijos + direcciones
    print('2. Probando endpoint consolidado...')
    response = requests.get(f'{BASE_URL}/users/1/children-and-addresses', headers=headers)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   ✅ Endpoint consolidado funciona')
        print(f'   Hijos: {len(data["hijos"])}, Direcciones: {len(data["direcciones"])}')
        if data['hijos']:
            print(f'   Primer hijo: {data["hijos"][0]}')
        if data['direcciones']:
            print(f'   Primera dirección: {data["direcciones"][0]}')
    else:
        print(f'   ❌ Error: {response.text}')
    
    # 3. Probar historial (debería fallar si no es premium)
    print('3. Probando historial (debería fallar para admin)...')
    response = requests.get(f'{BASE_URL}/history/', headers=headers)
    print(f'   Status esperado 403, obtenido: {response.status_code}')
    if response.status_code == 403:
        print('   ✅ Correcto: Admin no puede acceder a historial')
    else:
        print(f'   ❌ Problema: {response.text}')
    
    # 4. Probar crear un registro en historial
    print('4. Probando crear registro en historial...')
    historial_data = {
        'alimento_id': 1,
        'accion': 'eliminado',
        'motivo': 'Prueba del sistema'
    }
    response = requests.post(f'{BASE_URL}/history/', headers=headers, json=historial_data)
    print(f'   Status esperado 403, obtenido: {response.status_code}')
    if response.status_code == 403:
        print('   ✅ Correcto: Admin no puede crear en historial')
    else:
        print(f'   ❌ Problema: {response.text}')

if __name__ == '__main__':
    test_new_endpoints()
