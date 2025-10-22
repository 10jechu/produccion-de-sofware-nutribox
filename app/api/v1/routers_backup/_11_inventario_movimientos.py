from fastapi import APIRouter
from app.db.models.inventario_movimiento import Inventario_Movimiento

router = APIRouter(prefix="/api/v1/inventario_movimientos", tags=["11 - Inventario_Movimientos"])
