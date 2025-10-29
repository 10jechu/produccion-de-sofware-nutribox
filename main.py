from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import Base, engine

import app.db.models

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "auth", "description": "1️⃣ Registro e inicio de sesion"},
    {"name": "users", "description": "2️⃣ Gestion de perfil de usuario"},
    {"name": "children", "description": "3️⃣ Gestion de hijos"},
    {"name": "addresses", "description": "4️⃣ Direcciones de envio"},
    {"name": "restrictions", "description": "5️⃣ Restricciones alimentarias"},
    {"name": "foods", "description": "6️⃣ Catalogo de alimentos"},
    {"name": "lunchboxes", "description": "7️⃣ Loncheras escolares"},
    {"name": "menus_predeterminados", "description": "8️⃣ Menús Predeterminados (Admin)"},
]

app = FastAPI(
    title="NutriBox API",
    description="Plataforma para gestion de loncheras escolares - FASE 2",
    version="2.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite cualquier origen (para desarrollo)
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos HTTP
    allow_headers=["*"], # Permite todas las cabeceras
)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "env": settings.ENV, "app": "NutriBox API v2.0"}

from app.api.v1.routes import api_router
app.include_router(api_router)
