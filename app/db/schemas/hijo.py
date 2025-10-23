from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class HijoBase(BaseModel):
    nombre: str
    fecha_nacimiento: date

class HijoCreate(HijoBase):
    usuario_id: int

class HijoUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

class HijoRead(HijoBase):
    id: int
    usuario_id: int
    model_config = ConfigDict(from_attributes=True)
