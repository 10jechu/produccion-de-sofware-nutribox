from fastapi import APIRouter
from app.api.v1.routers import auth, foods, lunchboxes, addresses, restrictions, dev

api_router = APIRouter(prefix="/api/v1")

# Montar cada router una sola vez, sin prefijos extra
api_router.include_router(auth.router)
api_router.include_router(foods.router)
api_router.include_router(lunchboxes.router)
api_router.include_router(addresses.router)
api_router.include_router(restrictions.router)
api_router.include_router(dev.router)
