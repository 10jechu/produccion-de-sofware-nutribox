from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class AlimentoCreate(BaseModel):
    nombre: str = Field(alias="name")
    calorias: int = Field(ge=0, alias="calories")
    unidad: str = Field(default="g", alias="unit")
    model_config = ConfigDict(populate_by_name=True)

class AlimentoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, alias="name")
    calorias: Optional[int] = Field(default=None, ge=0, alias="calories")
    unidad: Optional[str] = Field(default=None, alias="unit")
    model_config = ConfigDict(populate_by_name=True)

class AlimentoRead(BaseModel):
    id: int
    nombre: str
    calorias: int
    unidad: str
    model_config = ConfigDict(from_attributes=True)
