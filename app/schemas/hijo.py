from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class HijoCreate(BaseModel):
    nombre: str
    fecha_nacimiento: date
    usuario_id: Optional[int] = None

class HijoUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    usuario_id: Optional[int] = None

class HijoRead(BaseModel):
    id: int
    nombre: str
    fecha_nacimiento: date
    usuario_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)
