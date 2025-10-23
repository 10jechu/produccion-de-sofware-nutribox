from pydantic import BaseModel
from app.db.schemas.common import ORMModel

class DireccionCreate(BaseModel):
    usuario_id: int
    etiqueta: str
    direccion: str
    barrio: str = ""
    ciudad: str = "Bogotá"

class DireccionUpdate(BaseModel):
    etiqueta: str | None = None
    direccion: str | None = None
    barrio: str | None = None
    ciudad: str | None = None

class DireccionRead(ORMModel):
    id: int
    usuario_id: int
    etiqueta: str
    direccion: str
    barrio: str
    ciudad: str
