"""Tests básicos sin dependencias complejas"""
import pytest
import uuid

def test_health(client):
    """Test del endpoint de salud"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print("\n✅ Health check OK")

def test_register_and_login(client):
    """Test de registro y login"""
    # Usar email único para evitar duplicados
    unique_email = f"testbasic_{uuid.uuid4().hex[:8]}@example.com"
    
    # Registro
    reg_response = client.post("/api/v1/auth/register", json={
        "nombre": "Test User",
        "email": unique_email,
        "password": "test123",
        "membresia": "Free",
        "rol": "Usuario"
    })
    assert reg_response.status_code in [200, 201]
    print(f"✅ Registro OK - {unique_email}")
    
    # Login
    login_response = client.post("/api/v1/auth/login", data={
        "username": unique_email,
        "password": "test123"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    print("✅ Login OK")

def test_foods_crud(client):
    """Test de CRUD de alimentos"""
    # Nombre único para evitar duplicados
    unique_name = f"Test Food {uuid.uuid4().hex[:6]}"
    
    # Crear
    create_response = client.post("/api/v1/foods", json={
        "nombre": unique_name,
        "kcal": 100,
        "proteinas": 5,
        "carbos": 20
    })
    assert create_response.status_code == 201
    food_id = create_response.json()["id"]
    print(f"✅ Alimento creado ID: {food_id}")
    
    # Listar
    list_response = client.get("/api/v1/foods")
    assert list_response.status_code == 200
    assert isinstance(list_response.json(), list)
    print("✅ Listar alimentos OK")
    
    # Obtener por ID
    get_response = client.get(f"/api/v1/foods/{food_id}")
    assert get_response.status_code == 200
    print("✅ Obtener alimento OK")

def test_users_list(client):
    """Test de listar usuarios"""
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("✅ Listar usuarios OK")
