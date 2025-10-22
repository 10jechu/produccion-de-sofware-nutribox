from pydantic import BaseModel, ConfigDict

class DireccionBase(BaseModel):
    etiqueta: str = "Casa"
    direccion: str
    barrio: str = ""
    ciudad: str = "Bogotá"

class DireccionCreate(DireccionBase):
    usuario_id: int

class DireccionUpdate(BaseModel):
    etiqueta: str | None = None
    direccion: str | None = None
    barrio: str | None = None
    ciudad: str | None = None

class DireccionRead(DireccionBase):
    id: int
    usuario_id: int
    
    model_config = ConfigDict(from_attributes=True)
