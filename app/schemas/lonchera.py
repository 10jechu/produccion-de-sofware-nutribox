from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class LoncheraCreate(BaseModel):
    hijo_id: int
    fecha: date

class LoncheraUpdate(BaseModel):
    hijo_id: Optional[int] = None
    fecha: Optional[date] = None
    estado: Optional[str] = None

class LoncheraRead(BaseModel):
    id: int
    hijo_id: int
    fecha: date
    estado: str
    direccion_id: Optional[int]
    model_config = ConfigDict(from_attributes=True)
