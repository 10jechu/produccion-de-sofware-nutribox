from pydantic import BaseModel, ConfigDict
from typing import Optional

class DireccionBase(BaseModel):
    etiqueta: str = "Casa"
    direccion: str
    barrio: str = ""
    ciudad: str = "Bogotá"

class DireccionCreate(DireccionBase):
    usuario_id: int

class DireccionUpdate(BaseModel):
    etiqueta: Optional[str] = None
    direccion: Optional[str] = None
    barrio: Optional[str] = None
    ciudad: Optional[str] = None

class DireccionRead(DireccionBase):
    id: int
    usuario_id: int
    model_config = ConfigDict(from_attributes=True)
