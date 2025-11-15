import requests

BASE_URL = "http://localhost:8000"

def check_endpoints():
    print("Verificando endpoints disponibles...")
    
    # Obtener OpenAPI schema
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            schema = response.json()
            paths = schema.get("paths", {})
            
            print("Endpoints de Admin Menus:")
            admin_menu_endpoints = [path for path in paths.keys() if "/admin/menus" in path]
            
            if admin_menu_endpoints:
                for endpoint in admin_menu_endpoints:
                    methods = list(paths[endpoint].keys())
                    print(f"  ✅ {endpoint} - {methods}")
            else:
                print("  ❌ No se encontraron endpoints de admin menus")
                
            print(f"Total de endpoints encontrados: {len(paths)}")
            return True
        else:
            print(f"Error obteniendo schema: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_endpoints()
