# -*- coding: utf-8 -*-
# scripts/smoke_api.py
import requests, time, random, string

BASE = "http://127.0.0.1:8000"
S = requests.Session()

def p(step, r):
    ok = "OK" if r.ok else f"ERROR ({r.status_code})"
    try:
        body = r.json()
    except Exception:
        body = r.text
    print(f"[{ok}] {step}\n  -> {body}\n")
    r.raise_for_status()
    return body

def wait_for_server(timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = requests.get(f"{BASE}/")
            if r.ok:
                print("Servidor listo.")
                return True
        except Exception:
            pass
        time.sleep(0.5)
    print("No pude conectar con el servidor. ¿Uvicorn está corriendo en 127.0.0.1:8000?")
    return False

def main():
    if not wait_for_server():
        return

    # 0) Opcional: reset/seed si tienes el router /dev activo
    try:
        p("DEV reset-db", S.post(f"{BASE}/api/v1/dev/reset-db"))
    except Exception:
        print("reset-db no disponible (continuo).")
    try:
        p("DEV seed", S.post(f"{BASE}/api/v1/dev/seed"))
    except Exception:
        print("seed no disponible (continuo).")

    # 1) Registro
    rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    email = f"smoke_{rand}@nutribox.test"
    password = "Test12345"

    payload_register = {
        "nombre": "Smoke Tester",
        "email": email,
        "password": password,
        "membresia": "Free",   # o "Premium"
        "rol": "Usuario"       # o "Admin"
    }
    user = p("Auth register", S.post(f"{BASE}/api/v1/auth/register", json=payload_register))
    user_id = user.get("id")

    # 2) Login (form-urlencoded)
    login_data = {
        "grant_type": "password",
        "username": email,
        "password": password
    }
    token = p("Auth login", S.post(f"{BASE}/api/v1/auth/login", data=login_data))
    access_token = token["access_token"]
    S.headers.update({"Authorization": f"Bearer {access_token}"})

    # 3) Foods
    food = p("Create food", S.post(f"{BASE}/api/v1/foods/", json={
        "nombre": "Manzana",
        "descripcion": "Fruta fresca rica en fibra",
        "calorias": 52,
        "proteinas": 0.3,
        "grasas": 0.2,
        "carbohidratos": 14
    }))
    food_id = food["id"]
    p("List foods", S.get(f"{BASE}/api/v1/foods/"))
    p("Update food", S.patch(f"{BASE}/api/v1/foods/{food_id}", json={"descripcion": "Fruta roja con antioxidantes"}))

    # 4) Address
    addr = p("Create address", S.post(f"{BASE}/api/v1/addresses/", json={
        "usuario_id": user_id,
        "etiqueta": "Casa",
        "direccion": "Cra 8 #123-45",
        "barrio": "Chapinero",
        "ciudad": "Bogotá"
    }))
    address_id = addr["id"]

    # 5) Lunchbox + item
    lunch = p("Create lunchbox", S.post(f"{BASE}/api/v1/lunchboxes/", json={
        "usuario_id": user_id,
        "nombre": "Lonchera saludable",
        "descripcion": "Comida balanceada de media mañana"
    }))
    lunch_id = lunch["id"]

    p("Add item to lunchbox", S.post(f"{BASE}/api/v1/lunchboxes/{lunch_id}/items", json={
        "alimento_id": food_id,
        "cantidad": 2
    }))

    p("Get lunchbox detail", S.get(f"{BASE}/api/v1/lunchboxes/{lunch_id}/detail"))

    # 6) Restrictions
    restr = p("Create restriction", S.post(f"{BASE}/api/v1/restrictions/", json={
        "usuario_id": user_id,
        "tipo": "Intolerancia",
        "descripcion": "Intolerancia a la lactosa"
    }))
    restriction_id = restr["id"]
    p("List restrictions", S.get(f"{BASE}/api/v1/restrictions/"))

    print("\n======== RESUMEN SMOKE TEST ========")
    print(f"Usuario    : {user_id}  ({email})")
    print(f"Food       : {food_id}")
    print(f"Address    : {address_id}")
    print(f"Lunchbox   : {lunch_id}")
    print(f"Restriction: {restriction_id}")
    print("API básico funcionando.")

if __name__ == "__main__":
    main()
