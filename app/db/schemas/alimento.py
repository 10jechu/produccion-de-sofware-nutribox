from pydantic import BaseModel, Field, ConfigDict

class AlimentoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    descripcion: str | None = None
    calorias: float = Field(ge=0)
    proteinas: float = Field(ge=0)
    grasas: float = Field(ge=0)
    carbohidratos: float = Field(ge=0)

class AlimentoCreate(AlimentoBase):
    pass

class AlimentoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    calorias: float | None = Field(default=None, ge=0)
    proteinas: float | None = Field(default=None, ge=0)
    grasas: float | None = Field(default=None, ge=0)
    carbohidratos: float | None = Field(default=None, ge=0)
    activo: bool | None = None

class AlimentoRead(AlimentoBase):
    id: int
    activo: bool
    
    model_config = ConfigDict(from_attributes=True)
