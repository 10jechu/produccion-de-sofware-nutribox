from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.routes import api_router
from app.db.session import engine
from app.db.models import Base

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API REST para gestión de loncheras escolares",
    openapi_tags=[
        {"name": "auth", "description": "Autenticación y registro"},
        {"name": "alimentos", "description": "Gestión de alimentos"},
        {"name": "loncheras", "description": "Gestión de loncheras"},
    ]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/", tags=["health"])
def health_check():
    """Endpoint de salud"""
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENV
    }

# Incluir routers
app.include_router(api_router)
