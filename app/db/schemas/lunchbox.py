from pydantic import BaseModel
from datetime import date
from app.db.schemas.common import ORMModel

class LoncheraCreate(BaseModel):
    hijo_id: int
    fecha: date
    estado: str = "Borrador"

class LoncheraRead(ORMModel):
    id: int
    hijo_id: int
    fecha: date
    estado: str

class LoncheraItemCreate(BaseModel):
    alimento_id: int
    cantidad: float = 1.0
