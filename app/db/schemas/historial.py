from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.db.schemas.common import ORMModel

class HistorialCreate(BaseModel):
    alimento_id: int
    accion: str
    motivo: Optional[str] = None

class HistorialRead(ORMModel):
    id: int
    alimento_id: int
    alimento_nombre: str
    usuario_id: int
    accion: str
    fecha: datetime
    motivo: Optional[str] = None

class HistorialReadWithAlimento(ORMModel):
    id: int
    alimento_id: int
    alimento_nombre: str
    alimento_kcal: float
    alimento_proteinas: float
    alimento_carbos: float
    usuario_id: int
    accion: str
    fecha: datetime
    motivo: Optional[str] = None
