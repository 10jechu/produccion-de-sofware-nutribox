import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    """Cliente de prueba para FastAPI"""
    return TestClient(app)

@pytest.fixture(scope="module")
def auth_headers(client):
    """Headers con token de autenticación"""
    # Primero registrar un usuario de prueba
    client.post("/api/v1/auth/register", json={
        "nombre": "Test User",
        "email": "test@example.com",
        "password": "test123",
        "membresia": "Premium",
        "rol": "Usuario"
    })
    
    # Hacer login
    response = client.post("/api/v1/auth/login", data={
        "username": "test@example.com",
        "password": "test123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
