# -*- coding: utf-8 -*-
import requests

BASE = "http://127.0.0.1:8000"

print("\n=== TEST NUTRIBOX API ===\n")

# 1. Health
print("1. Health Check...")
r = requests.get(f"{BASE}/")
print(f"   Status: {r.status_code} - {r.json()}\n")

# 2. Login
print("2. Login como admin...")
r = requests.post(f"{BASE}/api/v1/auth/login", 
    data={"username": "admin@nutribox.com", "password": "Admin123!"})
print(f"   Status: {r.status_code}")

if r.status_code == 200:
    token = r.json()["access_token"]
    print(f"   Token OK\n")
    
    # 3. Alimentos
    print("3. Listar alimentos...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE}/api/v1/alimentos/", headers=headers)
    print(f"   Status: {r.status_code}")
    
    if r.status_code == 200:
        alimentos = r.json()
        print(f"   Encontrados: {len(alimentos)} alimentos")
        for a in alimentos[:3]:
            print(f"     - {a['nombre']}")
    
    print("\n=== TESTS OK ===")
    print("\nDocumentacion: http://127.0.0.1:8000/docs")
else:
    print("   Error en login!")
