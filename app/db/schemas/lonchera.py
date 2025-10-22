from pydantic import BaseModel, ConfigDict
from datetime import date

class LoncheraBase(BaseModel):
    hijo_id: int
    fecha: date
    direccion_id: int | None = None

class LoncheraCreate(LoncheraBase):
    pass

class LoncheraUpdate(BaseModel):
    hijo_id: int | None = None
    fecha: date | None = None
    estado: str | None = None
    direccion_id: int | None = None

class LoncheraRead(LoncheraBase):
    id: int
    estado: str
    
    model_config = ConfigDict(from_attributes=True)

class LoncheraItemCreate(BaseModel):
    alimento_id: int
    cantidad: int = 1

class LoncheraItemUpdate(BaseModel):
    cantidad: int

class LoncheraItemRead(BaseModel):
    alimento_id: int
    nombre: str
    cantidad: int
    
    model_config = ConfigDict(from_attributes=True)

class DireccionMini(BaseModel):
    etiqueta: str
    direccion: str
    ciudad: str
