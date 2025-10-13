from fastapi import APIRouter
from app.api.v1.routers import foods, lunchboxes

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(foods.router, prefix="/foods", tags=["foods"])
api_router.include_router(lunchboxes.router, prefix="/lunchboxes", tags=["lunchboxes"])
