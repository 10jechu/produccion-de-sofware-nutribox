import requests

BASE_URL = 'http://localhost:8000/api/v1'

def final_backend_check():
    print("🎯 VERIFICACIÓN FINAL BACKEND")
    print("=" * 40)
    
    # Login de admin
    try:
        login_data = {'username': 'admin@nutribox.com', 'password': 'admin123'}
        response = requests.post(f'{BASE_URL}/auth/login', data=login_data)
        
        if response.status_code != 200:
            print("❌ Error en login")
            return False
        
        token = response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print("✅ Login exitoso")
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    checks = [
        ("Menús Admin", f"{BASE_URL}/admin/menus/", "GET", None, 200),
        ("Endpoint Consolidado", f"{BASE_URL}/users/1/children-and-addresses", "GET", None, 200),
        ("Historial (debe fallar para admin)", f"{BASE_URL}/history/", "GET", None, 403),
        ("Alimentos", f"{BASE_URL}/foods/", "GET", None, 200),
        ("Crear Menú", f"{BASE_URL}/admin/menus/", "POST", {
            'nombre': 'Menu Test Final',
            'descripcion': 'Menu de prueba final',
            'dia_semana': 'Lunes',
            'alimentos': []
        }, 201)
    ]
    
    all_ok = True
    for check_name, url, method, data, expected_status in checks:
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            
            status_ok = response.status_code == expected_status
            status_icon = "✅" if status_ok else "❌"
            print(f"{status_icon} {check_name}: {response.status_code} (esperado: {expected_status})")
            
            if not status_ok:
                print(f"   Detalle: {response.text}")
                all_ok = False
                
        except Exception as e:
            print(f"❌ {check_name}: Error - {e}")
            all_ok = False
    
    print(f"\n🎯 BACKEND: {'✅ COMPLETAMENTE FUNCIONAL' if all_ok else '❌ REVISAR ERRORES'}")
    
    if all_ok:
        print("\n🚀 ¡BACKEND LISTO! Proceder con correcciones del Frontend Vue.js")
        print("   📋 Próximos pasos:")
        print("   1. Corregir 'Crear Lonchera' - Usar endpoint consolidado")
        print("   2. Aplicar permisos por membresía en frontend")
        print("   3. Fix panel lateral (hacerlo fijo)")
        print("   4. Agregar mensajes para funciones restringidas")
    
    return all_ok

if __name__ == "__main__":
    final_backend_check()
