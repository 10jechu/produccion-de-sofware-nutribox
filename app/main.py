# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.db.database import Base, engine

# Registra TODOS los modelos (core_models, alimento, lunchbox, etc.)
import app.db.models  # noqa: F401

# Crea tablas automáticamente en DEV (en PROD usa migraciones/Alembic)
Base.metadata.create_all(bind=engine)

# FastAPI app
tags_metadata = [
    {"name": "auth",         "description": "Registro e inicio de sesión"},
    {"name": "foods",        "description": "Catálogo de alimentos"},
    {"name": "lunchboxes",   "description": "Loncheras e items"},
    {"name": "addresses",    "description": "Direcciones de envío"},
    {"name": "restrictions", "description": "Restricciones alimentarias"},
    {"name": "dev",          "description": "Herramientas para desarrollo"},
]
app = FastAPI(openapi_tags=tags_metadata, title="NutriBox API")

@app.get("/")
def health():
    return {"status": "ok", "env": settings.ENV}

# Rutas v1
from app.api.v1.routes import api_router
app.include_router(api_router)
