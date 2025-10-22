from pydantic import BaseModel, Field
from app.db.schemas.common import ORMModel

class AlimentoBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    kcal: float
    proteinas: float
    carbos: float

class AlimentoCreate(AlimentoBase): pass

class AlimentoUpdate(BaseModel):
    nombre: str | None = None
    kcal: float | None = None
    proteinas: float | None = None
    carbos: float | None = None
    activo: bool | None = None

class AlimentoRead(ORMModel, AlimentoBase):
    id: int
    activo: bool
