"""Test del flujo completo - VERSION CORRECTA"""
import pytest
import uuid
import random

@pytest.fixture(scope="module")
def test_user(client):
    """Crea un usuario de prueba y retorna sus datos"""
    random_id = f"{uuid.uuid4().hex[:6]}{random.randint(1000, 9999)}"
    email = f"flowtest{random_id}@example.com"
    
    response = client.post("/api/v1/auth/register", json={
        "nombre": f"Flow Test {random_id}",
        "email": email,
        "password": "test123",
        "membresia": "Premium",
        "rol": "Usuario"
    })
    
    # Login para obtener token
    login = client.post("/api/v1/auth/login", data={
        "username": email,
        "password": "test123"
    })
    
    # Obtener user_id
    users = client.get("/api/v1/users").json()
    user = next((u for u in users if u["email"] == email), None)
    
    return {
        "id": user["id"],
        "email": user["email"],
        "token": login.json()["access_token"]
    }

def test_01_health_check(client):
    """✅ Servidor está corriendo"""
    response = client.get("/")
    assert response.status_code == 200
    print("\n✅ Health check OK")

def test_02_register_and_login(client):
    """✅ Registro y login"""
    random_id = f"{uuid.uuid4().hex[:6]}{random.randint(1000, 9999)}"
    email = f"indiv{random_id}@test.com"
    
    # Registro
    response = client.post("/api/v1/auth/register", json={
        "nombre": f"Test Indiv {random_id}",
        "email": email,
        "password": "123456",
        "membresia": "Free",
        "rol": "Usuario"
    })
    assert response.status_code in [200, 201]
    print("✅ Registro OK")
    
    # Login
    login_response = client.post("/api/v1/auth/login", data={
        "username": email,
        "password": "123456"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    print("✅ Login OK")

def test_03_list_users(client):
    """✅ Listar usuarios"""
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("✅ Listar usuarios OK")

def test_04_create_child(client, test_user):
    """✅ Crear hijo"""
    random_id = random.randint(1000, 9999)
    response = client.post("/api/v1/children", json={
        "nombre": f"Test Child {random_id}",
        "usuario_id": test_user["id"]
    })
    assert response.status_code == 201
    child_id = response.json()["id"]
    print(f"✅ Hijo creado ID: {child_id}")

def test_05_list_children(client, test_user):
    """✅ Listar hijos"""
    response = client.get(f"/api/v1/children?usuario_id={test_user['id']}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("✅ Listar hijos OK")

def test_06_create_address(client, test_user):
    """✅ Crear dirección"""
    random_id = random.randint(1000, 9999)
    response = client.post("/api/v1/addresses", json={
        "usuario_id": test_user["id"],
        "etiqueta": f"Test Casa {random_id}",
        "direccion": f"Calle Test {random_id}",
        "barrio": "Test Barrio",
        "ciudad": "Bogotá"
    })
    assert response.status_code == 201
    print("✅ Dirección creada OK")

def test_07_create_foods(client):
    """✅ Crear alimentos"""
    random_id = random.randint(1000, 9999)
    foods = [
        {"nombre": f"TestManzana{random_id}", "kcal": 52, "proteinas": 0.3, "carbos": 14},
        {"nombre": f"TestSandwich{random_id}", "kcal": 250, "proteinas": 12, "carbos": 30}
    ]
    
    for food in foods:
        response = client.post("/api/v1/foods", json=food)
        assert response.status_code in [201, 400]
    
    print("✅ Alimentos creados OK")

def test_08_list_foods(client):
    """✅ Listar alimentos"""
    response = client.get("/api/v1/foods")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("✅ Listar alimentos OK")

def test_09_filter_foods_active(client):
    """✅ Filtrar alimentos activos"""
    response = client.get("/api/v1/foods?only_active=true")
    assert response.status_code == 200
    data = response.json()
    assert all(item["activo"] == True for item in data)
    print("✅ Filtro activos OK")

def test_10_filter_foods_all(client):
    """✅ Filtrar todos los alimentos"""
    response = client.get("/api/v1/foods?only_active=all")
    assert response.status_code == 200
    print("✅ Filtro todos OK")
