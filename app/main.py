from fastapi import FastAPI
from app.core.config import settings
from app.db.database import Base, engine

import app.db.models

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "auth", "description": "Registro e inicio de sesion"},
    {"name": "users", "description": "Gestion de usuarios (Admin)"},
    {"name": "children", "description": "Gestion de hijos"},
    {"name": "foods", "description": "Catalogo de alimentos"},
    {"name": "lunchboxes", "description": "Loncheras e items"},
    {"name": "addresses", "description": "Direcciones de envio"},
    {"name": "restrictions", "description": "Restricciones alimentarias"},
]

app = FastAPI(
    title="NutriBox API",
    description="Plataforma para gestion de loncheras escolares",
    version="1.0.0",
    openapi_tags=tags_metadata
)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "env": settings.ENV, "app": "NutriBox API"}

from app.api.v1.routes import api_router
app.include_router(api_router)