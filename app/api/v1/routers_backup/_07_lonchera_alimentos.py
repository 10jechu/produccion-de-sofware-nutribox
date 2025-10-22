from fastapi import APIRouter
from app.db.models.lonchera_alimento import Lonchera_Alimento

router = APIRouter(prefix="/api/v1/lonchera_alimentos", tags=["07 - Lonchera_Alimentos"])
