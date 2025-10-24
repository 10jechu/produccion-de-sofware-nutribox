from fastapi import APIRouter
from app.api.v1.routers import auth, users, children, addresses, restrictions, foods, lunchboxes

api_router = APIRouter(prefix="/api/v1")

# Orden lógico del flujo del usuario
api_router.include_router(auth.router)         # 1. Autenticación
api_router.include_router(users.router)        # 2. Perfil
api_router.include_router(children.router)     # 3. Hijos
api_router.include_router(addresses.router)    # 4. Direcciones
api_router.include_router(restrictions.router) # 5. Restricciones
api_router.include_router(foods.router)        # 6. Alimentos
api_router.include_router(lunchboxes.router)   # 7. Loncheras
