# ��� NutriBox - Sistema de Gestión de Loncheras Escolares

## ��� Descripción
NutriBox es una plataforma web para la gestión y personalización de loncheras escolares, desarrollada con FastAPI y SQLAlchemy.

## ��� Inicio Rápido

### Requisitos Previos
- Python 3.10+
- pip

### Instalación

1. Clonar el repositorio:
```bash
git clone <tu-repo>
cd produccion-de-sofware-nutribox
```

2. Crear entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Poblar base de datos:
```bash
python scripts/seed_db.py
```

5. Ejecutar servidor:
```bash
uvicorn app.main:app --reload --port 8000
```

6. Acceder a:
- API: http://127.0.0.1:8000
- Documentación: http://127.0.0.1:8000/docs

## ��� Credenciales de Prueba

**Administrador:**
- Email: `admin@nutribox.com`
- Password: `Admin123!`

## ��� Estructura del Proyecto
```
nutribox/
├── app/
│   ├── api/v1/
│   │   └── routers/      # Endpoints de la API
│   ├── core/             # Configuración y seguridad
│   ├── crud/             # Operaciones de BD
│   ├── db/
│   │   ├── models/       # Modelos SQLAlchemy
│   │   └── schemas/      # Esquemas Pydantic
│   └── main.py           # Aplicación FastAPI
├── scripts/              # Scripts de utilidad
├── tests/                # Pruebas
└── requirements.txt      # Dependencias
```

## ���️ Endpoints Principales

### Autenticación
- `POST /api/v1/auth/register` - Registrar usuario
- `POST /api/v1/auth/login` - Iniciar sesión
- `GET /api/v1/auth/me` - Info del usuario actual

### Alimentos
- `GET /api/v1/alimentos/` - Listar alimentos
- `POST /api/v1/alimentos/` - Crear alimento (Admin)
- `GET /api/v1/alimentos/{id}` - Obtener alimento
- `PATCH /api/v1/alimentos/{id}` - Actualizar alimento (Admin)
- `DELETE /api/v1/alimentos/{id}` - Eliminar alimento (Admin)

### Loncheras
- `GET /api/v1/loncheras/` - Listar loncheras
- `POST /api/v1/loncheras/` - Crear lonchera
- `GET /api/v1/loncheras/{id}` - Obtener lonchera
- `PATCH /api/v1/loncheras/{id}` - Actualizar lonchera
- `DELETE /api/v1/loncheras/{id}` - Eliminar lonchera
- `POST /api/v1/loncheras/{id}/items` - Agregar alimento
- `DELETE /api/v1/loncheras/{id}/items/{alimento_id}` - Quitar alimento
- `GET /api/v1/loncheras/{id}/items` - Listar items

## ��� Testing
```bash
# Test manual de endpoints
python scripts/test_api.py

# Tests con pytest (cuando se implementen)
pytest
```

## ��� Documentación

La documentación interactiva está disponible en:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## ��� Equipo

- Julián Steven Leal - 67001277
- Luis David Rubio Ramírez - 67001331
- Jesús Manuel Vilardi González - 67001298

## ��� Licencia

Universidad Católica de Colombia - 2025
