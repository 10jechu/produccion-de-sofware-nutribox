from pydantic import BaseModel
from datetime import date
from app.db.schemas.common import ORMModel

class LoncheraCreate(BaseModel):
    hijo_id: int
    fecha: date
    estado: str = "Borrador"
    direccion_id: int | None = None

class LoncheraUpdate(BaseModel):
    fecha: date | None = None
    estado: str | None = None
    direccion_id: int | None = None

class LoncheraRead(ORMModel):
    id: int
    hijo_id: int
    fecha: date
    estado: str
    direccion_id: int | None

class LoncheraItemCreate(BaseModel):
    alimento_id: int
    cantidad: float = 1.0

class LoncheraItemUpdate(BaseModel):
    cantidad: float

class LoncheraItemRead(ORMModel):
    lonchera_id: int
    alimento_id: int
    cantidad: float
