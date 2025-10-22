from fastapi import APIRouter
from app.db.models.historial_alimento import Historial_Alimento

router = APIRouter(prefix="/api/v1/historial_alimentos", tags=["12 - Historial_Alimentos"])
