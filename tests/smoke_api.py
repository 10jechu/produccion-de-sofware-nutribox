"""
Smoke test end-to-end: registra usuario, hace login,
crea alimento, dirección, lonchera, item y restricción.
Al final limpia (borra) lo creado.
Requiere que el servidor esté corriendo en 127.0.0.1:8000
"""
import requests, random, string, sys

BASE = "http://127.0.0.1:8000"
S = requests.Session()

def p(step, resp):
    ok = "✅" if resp.ok else f"❌ ({resp.status_code})"
    try:
        body = resp.json()
    except Exception:
        body = resp.text
    print(f"[{ok}] {step}\n  -> {body}\n")
    resp.raise_for_status()
    return body

def rand_email():
    r = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"smoke_{r}@nutribox.test"

def main():
    user_id = food_id = address_id = lunch_id = restriction_id = None
    try:
        # ---------- DEV: intenta seedear (no es obligatorio) ----------
        try:
            p("DEV seed", S.post(f"{BASE}/api/v1/dev/seed"))
        except Exception:
            print("⚠️  /api/v1/dev/seed no disponible (continuo).")

        # ---------- 1) Register ----------
        email = rand_email()
        password = "Test12345"
        reg_payload = {
            "nombre": "Smoke Tester",
            "email": email,
            "password": password,
            "membresia": "Free",   # "Free" o "Premium"
            "rol": "Usuario"       # "Usuario" o "Admin"
        }
        reg = p("Auth register", S.post(f"{BASE}/api/v1/auth/register", json=reg_payload))
        user_id = reg.get("id")

        # ---------- 2) Login ----------
        login_form = {
            "grant_type": "password",
            "username": email,
            "password": password
        }
        token = p("Auth login", S.post(f"{BASE}/api/v1/auth/login", data=login_form))
        access = token["access_token"]
        S.headers.update({"Authorization": f"Bearer {access}"})

        # ---------- 3) Foods ----------
        food = p("Create food", S.post(f"{BASE}/api/v1/foods/", json={
            "nombre": "Manzana",
            "descripcion": "Fruta fresca rica en fibra",
            "calorias": 52,
            "proteinas": 0.3,
            "grasas": 0.2,
            "carbohidratos": 14
        }))
        food_id = food["id"]

        _ = p("List foods", S.get(f"{BASE}/api/v1/foods/"))
        _ = p("Update food", S.patch(f"{BASE}/api/v1/foods/{food_id}", json={
            "descripcion": "Fruta roja con antioxidantes"
        }))

        # ---------- 4) Address ----------
        addr = p("Create address", S.post(f"{BASE}/api/v1/addresses/", json={
            "usuario_id": user_id,
            "etiqueta": "Casa",
            "direccion": "Cra 8 #123-45",
            "barrio": "Chapinero",
            "ciudad": "Bogotá"
        }))
        address_id = addr["id"]

        # ---------- 5) Lunchbox + item ----------
        lunch = p("Create lunchbox", S.post(f"{BASE}/api/v1/lunchboxes/", json={
            "usuario_id": user_id,
            "nombre": "Lonchera saludable",
            "descripcion": "Comida balanceada de media mañana"
        }))
        lunch_id = lunch["id"]

        _ = p("Add item to lunchbox", S.post(f"{BASE}/api/v1/lunchboxes/{lunch_id}/items", json={
            "alimento_id": food_id,
            "cantidad": 2
        }))

        _ = p("Get lunchbox detail", S.get(f"{BASE}/api/v1/lunchboxes/{lunch_id}/detail"))

        # ---------- 6) Restrictions ----------
        restr = p("Create restriction", S.post(f"{BASE}/api/v1/restrictions/", json={
            "usuario_id": user_id,
            "tipo": "Intolerancia",
            "descripcion": "Intolerancia a la lactosa"
        }))
        restriction_id = restr["id"]

        _ = p("List restrictions", S.get(f"{BASE}/api/v1/restrictions/"))

        print("\n======== RESUMEN SMOKE TEST ========")
        print(f"Usuario     : {user_id}  ({email})")
        print(f"Food        : {food_id}")
        print(f"Address     : {address_id}")
        print(f"Lunchbox    : {lunch_id}")
        print(f"Restriction : {restriction_id}")
        print("✅ API básico funcionando.\n")

    finally:
        # ---------- Limpieza (best effort) ----------
        try:
            # si existe endpoint DEV para borrar usuario con todo:
            if user_id:
                p("DEV delete user (cascade)", S.delete(f"{BASE}/api/v1/dev/users/{user_id}"))
        except Exception as e:
            print(f"⚠️  Limpieza DEV falló: {e}")

        # (si tuvieras que limpiar manualmente, descomenta lo siguiente):
        # try:
        #     if restriction_id:
        #         p("Delete restriction", S.delete(f"{BASE}/api/v1/restrictions/{restriction_id}"))
        #     if lunch_id:
        #         p("Delete lunchbox", S.delete(f"{BASE}/api/v1/lunchboxes/{lunch_id}"))
        #     if address_id:
        #         p("Delete address", S.delete(f"{BASE}/api/v1/addresses/{address_id}"))
        #     if food_id:
        #         p("Delete food", S.delete(f"{BASE}/api/v1/foods/{food_id}"))
        # except Exception as e:
        #     print(f"⚠️  Limpieza manual falló: {e}")

if __name__ == "__main__":
    try:
        main()
    except requests.ConnectionError:
        print("❌ No puedo conectar al servidor. ¿Uvicorn está corriendo en 127.0.0.1:8000?")
        sys.exit(1)
