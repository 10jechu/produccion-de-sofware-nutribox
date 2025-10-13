from pydantic import BaseModel
from app.db.schemas.common import ORMModel

class DireccionCreate(BaseModel):
    usuario_id: int
    etiqueta: str
    direccion: str
    barrio: str = ""
    ciudad: str = "Bogotá"

class DireccionRead(ORMModel):
    id: int
    usuario_id: int
    etiqueta: str
    direccion: str
    barrio: str
    ciudad: str
