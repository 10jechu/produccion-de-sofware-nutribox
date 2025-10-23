from pydantic import BaseModel, Field
from app.db.schemas.common import ORMModel

class HijoCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    usuario_id: int

class HijoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=2, max_length=120)

class HijoRead(ORMModel):
    id: int
    nombre: str
    usuario_id: int
