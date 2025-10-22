from fastapi import APIRouter
from app.api.v1.routers import auth, alimentos, loncheras

api_router = APIRouter(prefix="/api/v1")

# Incluir todos los routers
api_router.include_router(auth.router)
api_router.include_router(alimentos.router)
api_router.include_router(loncheras.router)
