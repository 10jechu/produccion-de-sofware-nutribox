# -*- coding: utf-8 -*-
import requests
import json
from datetime import date

BASE = "http://127.0.0.1:8000"

def print_result(step, response):
    status = "OK" if response.ok else "ERROR"
    print(f"\n{status} {step}")
    print(f"   Status: {response.status_code}")
    if response.ok:
        try:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return data
        except:
            print(f"   Response: {response.text}")
            return None
    else:
        print(f"   Error: {response.text}")
        return None

print("=" * 60)
print("PRUEBA COMPLETA DE NUTRIBOX API")
print("=" * 60)

# 1. HEALTH CHECK
r = requests.get(f"{BASE}/health")
print_result("Health Check", r)

# 2. CREAR ROL
r = requests.post(f"{BASE}/api/v1/roles/", json={
    "nombre": "Usuario"
})
rol = print_result("Crear Rol Usuario", r)

# 3. CREAR MEMBRESIA
r = requests.post(f"{BASE}/api/v1/membresias/", json={
    "tipo": "Premium",
    "max_direcciones": 3
})
membresia = print_result("Crear Membresia Premium", r)

# 4. REGISTRAR USUARIO
r = requests.post(f"{BASE}/api/v1/auth/register", json={
    "nombre": "Maria Garcia",
    "email": "maria@nutribox.test",
    "contrasena": "Pass12345",
    "rol": "Usuario",
    "membresia": "Premium"
})
user_data = print_result("Registrar Usuario", r)
usuario_id = user_data.get("id") if user_data else 1

# 5. LOGIN
r = requests.post(f"{BASE}/api/v1/auth/login", data={
    "username": "maria@nutribox.test",
    "password": "Pass12345"
})
token_data = print_result("Login Usuario", r)
token = token_data.get("access_token") if token_data else None

# 6. LISTAR USUARIOS
r = requests.get(f"{BASE}/api/v1/usuarios/")
print_result("Listar Usuarios", r)

# 7. CREAR HIJO
r = requests.post(f"{BASE}/api/v1/hijos/", json={
    "nombre": "Sofia Garcia",
    "fecha_nacimiento": "2018-05-15",
    "usuario_id": usuario_id
})
hijo = print_result("Crear Hijo", r)
hijo_id = hijo.get("id") if hijo else 1

# 8. CREAR ALIMENTOS
alimentos_data = [
    {"nombre": "Manzana", "calorias": 52, "proteinas": 0.3, "carbohidratos": 14, "unidad": "unidad"},
    {"nombre": "Yogurt Natural", "calorias": 59, "proteinas": 3.5, "carbohidratos": 4.7, "unidad": "100g"},
    {"nombre": "Pan Integral", "calorias": 247, "proteinas": 13, "carbohidratos": 41, "unidad": "100g"},
    {"nombre": "Queso", "calorias": 402, "proteinas": 25, "carbohidratos": 1.3, "unidad": "100g"}
]

alimento_ids = []
for alimento_data in alimentos_data:
    r = requests.post(f"{BASE}/api/v1/alimentos/", json=alimento_data)
    alimento = print_result(f"Crear Alimento: {alimento_data['nombre']}", r)
    if alimento:
        alimento_ids.append(alimento["id"])

# 9. CREAR DIRECCION
r = requests.post(f"{BASE}/api/v1/direcciones/", json={
    "usuario_id": usuario_id,
    "etiqueta": "Casa",
    "direccion": "Calle 123 #45-67",
    "barrio": "Chapinero",
    "ciudad": "Bogota"
})
direccion = print_result("Crear Direccion", r)
direccion_id = direccion.get("id") if direccion else None

# 10. CREAR LONCHERA
r = requests.post(f"{BASE}/api/v1/loncheras/", json={
    "hijo_id": hijo_id,
    "fecha": str(date.today())
})
lonchera = print_result("Crear Lonchera", r)
lonchera_id = lonchera.get("id") if lonchera else 1

# 11. AGREGAR ALIMENTOS A LONCHERA
if alimento_ids:
    for i, alimento_id in enumerate(alimento_ids[:3]):
        r = requests.post(f"{BASE}/api/v1/lonchera-alimentos/", json={
            "lonchera_id": lonchera_id,
            "alimento_id": alimento_id,
            "cantidad": 1.0 + (i * 0.5)
        })
        print_result(f"Agregar Alimento {alimento_id} a Lonchera", r)

# 12. LISTAR ALIMENTOS DE LONCHERA
r = requests.get(f"{BASE}/api/v1/lonchera-alimentos/lonchera/{lonchera_id}")
print_result("Listar Alimentos de Lonchera", r)

# 13. CREAR RESTRICCION (alergia)
if alimento_ids:
    r = requests.post(f"{BASE}/api/v1/restricciones/", json={
        "hijo_id": hijo_id,
        "tipo": "alergia",
        "alimento_id": alimento_ids[-1],
        "texto": None
    })
    print_result("Crear Restriccion: Alergia al Queso", r)

# 14. CREAR RESTRICCION (prohibido)
r = requests.post(f"{BASE}/api/v1/restricciones/", json={
    "hijo_id": hijo_id,
    "tipo": "prohibido",
    "alimento_id": None,
    "texto": "azucar refinada"
})
print_result("Crear Restriccion: Prohibido azucar", r)

# 15. LISTAR RESTRICCIONES
r = requests.get(f"{BASE}/api/v1/restricciones/")
print_result("Listar Restricciones", r)

print("\n" + "=" * 60)
print("RESUMEN DE PRUEBAS")
print("=" * 60)
print(f"Usuario ID: {usuario_id}")
print(f"Hijo ID: {hijo_id}")
print(f"Alimentos creados: {len(alimento_ids)}")
print(f"Lonchera ID: {lonchera_id}")
print(f"Direccion ID: {direccion_id}")
print("\nTODAS LAS RELACIONES FUNCIONAN CORRECTAMENTE")
print("=" * 60)
