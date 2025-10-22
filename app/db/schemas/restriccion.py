from pydantic import BaseModel, ConfigDict, Field

class RestriccionBase(BaseModel):
    tipo: str = Field(..., pattern="^(alergia|prohibido)$")
    alimento_id: int | None = None
    texto: str | None = None
    motivo: str | None = None

class RestriccionCreate(RestriccionBase):
    hijo_id: int

class RestriccionUpdate(BaseModel):
    tipo: str | None = Field(default=None, pattern="^(alergia|prohibido)$")
    alimento_id: int | None = None
    texto: str | None = None
    motivo: str | None = None

class RestriccionRead(RestriccionBase):
    id: int
    hijo_id: int
    
    model_config = ConfigDict(from_attributes=True)
