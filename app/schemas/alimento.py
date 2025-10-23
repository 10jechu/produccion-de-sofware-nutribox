from pydantic import BaseModel, ConfigDict
from typing import Optional

class AlimentoCreate(BaseModel):
    nombre: str
    calorias: int = 0
    proteinas: float = 0.0
    carbohidratos: float = 0.0
    unidad: str = "g"

class AlimentoUpdate(BaseModel):
    nombre: Optional[str] = None
    calorias: Optional[int] = None
    proteinas: Optional[float] = None
    carbohidratos: Optional[float] = None
    unidad: Optional[str] = None

class AlimentoRead(BaseModel):
    id: int
    nombre: str
    calorias: int
    proteinas: float
    carbohidratos: float
    unidad: str
    activo: bool
    model_config = ConfigDict(from_attributes=True)
