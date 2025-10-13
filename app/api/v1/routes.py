from fastapi import APIRouter
from app.api.v1.routers import foods, lunchboxes, addresses, restrictions, dev

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(foods.router,        prefix="/foods",        tags=["foods"])
api_router.include_router(lunchboxes.router,   prefix="/lunchboxes",   tags=["lunchboxes"])
api_router.include_router(addresses.router,    prefix="/addresses",    tags=["addresses"])
api_router.include_router(restrictions.router, prefix="/restrictions", tags=["restrictions"])
api_router.include_router(dev.router,          prefix="/dev",          tags=["dev"])
