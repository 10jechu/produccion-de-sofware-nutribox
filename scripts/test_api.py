# -*- coding: utf-8 -*-
"""Script para probar los endpoints principales"""
import sys
from pathlib import Path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def print_separator(title=""):
    print("\n" + "="*60)
    if title:
        print(f"  {title}")
        print("="*60)
    else:
        print("="*60)

def test_health():
    print("\nTest: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_register():
    print("\nTest: Registro de usuario")
    data = {
        "full_name": "Usuario Test",
        "email": "test@nutribox.com",
        "password": "Test1234!",
        "rol": "Usuario",
        "membresia": "Free"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [200, 201, 400]
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    print("\nTest: Login")
    data = {
        "username": "admin@nutribox.com",
        "password": "Admin123!"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", data=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"Token obtenido: {token[:30]}...")
            return token
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_me(token):
    print("\nTest: Info usuario actual")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_alimentos(token):
    print("\nTest: Listar alimentos")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/api/v1/alimentos/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            alimentos = response.json()
            print(f"Alimentos encontrados: {len(alimentos)}")
            if alimentos:
                print(f"Primeros 3 alimentos:")
                for alimento in alimentos[:3]:
                    print(f"  - {alimento['nombre']}: {alimento['calorias']} kcal")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_crear_alimento(token):
    print("\nTest: Crear alimento")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "nombre": "Uvas",
        "descripcion": "Racimo de uvas frescas",
        "calorias": 69,
        "proteinas": 0.7,
        "grasas": 0.2,
        "carbohidratos": 18
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/alimentos/", json=data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"Alimento creado: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_loncheras(token):
    print("\nTest: Crear lonchera")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "hijo_id": 1,
        "fecha": "2025-01-30"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/loncheras/", json=data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print_separator("TESTING NUTRIBOX API")
    
    # 1. Health check
    health_ok = test_health()
    if not health_ok:
        print("\nEl servidor no esta respondiendo. Esta corriendo uvicorn?")
        return
    
    # 2. Register
    test_register()
    
    # 3. Login y obtener token
    token = test_login()
    if not token:
        print("\nNo se pudo obtener el token. Revisa las credenciales.")
        return
    
    # 4. Tests con autenticacion
    print_separator("Tests con autenticacion")
    test_me(token)
    test_alimentos(token)
    test_crear_alimento(token)
    
    print_separator("Tests completados")
    print("\nPara mas pruebas, abre: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    main()
