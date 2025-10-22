from pydantic import BaseModel, ConfigDict
from datetime import date

class HijoBase(BaseModel):
    nombre: str
    fecha_nacimiento: date

class HijoCreate(HijoBase):
    usuario_id: int

class HijoUpdate(BaseModel):
    nombre: str | None = None
    fecha_nacimiento: date | None = None

class HijoRead(HijoBase):
    id: int
    usuario_id: int
    
    model_config = ConfigDict(from_attributes=True)
