from typing import Optional
from pydantic import BaseModel, ConfigDict

class HijoCreate(BaseModel):
    nombre: str
    fecha_nacimiento: str
    usuario_id: int

class HijoUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha_nacimiento: Optional[str] = None

class HijoRead(BaseModel):
    id: int
    nombre: str
    fecha_nacimiento: str
    usuario_id: int
    model_config = ConfigDict(from_attributes=True)
