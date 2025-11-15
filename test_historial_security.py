import requests

BASE_URL = 'http://localhost:8000/api/v1'

def test_historial_security():
    print("🔒 PROBANDO SEGURIDAD DEL HISTORIAL")
    print("=" * 40)
    
    # 1. Probar con admin (debe fallar)
    print("1. Probando con usuario Admin...")
    admin_login = {'username': 'admin@nutribox.com', 'password': 'admin123'}
    response = requests.post(f'{BASE_URL}/auth/login', data=admin_login)
    
    if response.status_code == 200:
        admin_token = response.json()['access_token']
        admin_headers = {'Authorization': f'Bearer {admin_token}'}
        
        response = requests.get(f'{BASE_URL}/history/', headers=admin_headers)
        print(f"   Admin → Historial: {response.status_code} (esperado: 403)")
        if response.status_code == 403:
            print("   ✅ Correcto: Admin no puede acceder al historial")
        else:
            print(f"   ❌ Problema: Admin pudo acceder - {response.text}")
    else:
        print("   ❌ Error login admin")
    
    # 2. Probar con usuario premium (debe funcionar)
    print("\n2. Probando con usuario Premium...")
    premium_login = {'username': 'premium@test.com', 'password': 'premium123'}
    response = requests.post(f'{BASE_URL}/auth/login', data=premium_login)
    
    if response.status_code == 200:
        premium_token = response.json()['access_token']
        premium_headers = {'Authorization': f'Bearer {premium_token}'}
        
        response = requests.get(f'{BASE_URL}/history/', headers=premium_headers)
        print(f"   Premium → Historial: {response.status_code} (esperado: 200)")
        if response.status_code == 200:
            print("   ✅ Correcto: Premium puede acceder al historial")
        else:
            print(f"   ❌ Problema: Premium no pudo acceder - {response.text}")
    else:
        print("   ❌ Error login premium")

if __name__ == "__main__":
    test_historial_security()
