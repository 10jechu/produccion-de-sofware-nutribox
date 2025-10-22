from app.middlewares.normalize_body import normalize_body_middleware
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

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000","http://localhost:8000","http://127.0.0.1:8001","http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(normalize_body_middleware)

@app.get("/")
def health():
    return {"status": "ok", "env": settings.ENV}

# Rutas v1
from app.api.v1.routes import api_router
app.include_router(api_router)