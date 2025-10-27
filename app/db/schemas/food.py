from pydantic import BaseModel, Field
from app.db.schemas.common import ORMModel

class AlimentoCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    kcal: float = Field(ge=0)
    proteinas: float = Field(ge=0)
    carbos: float = Field(ge=0)
    costo: float = Field(ge=0, default=0.0) # NUEVO CAMPO
    
class AlimentoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=2, max_length=120)
    kcal: float | None = Field(None, ge=0)
    proteinas: float | None = Field(None, ge=0)
    carbos: float | None = Field(None, ge=0)
    costo: float | None = Field(None, ge=0) # NUEVO CAMPO
    activo: bool | None = None

class AlimentoRead(ORMModel):
    id: int
    nombre: str
    kcal: float
    proteinas: float
    carbos: float
    costo: float # NUEVO CAMPO
    activo: bool
