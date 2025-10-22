from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class LoncheraCreate(BaseModel):
    hijo_id: int
    fecha: date  # formato: "YYYY-MM-DD"

class LoncheraUpdate(BaseModel):
    hijo_id: Optional[int] = None
    fecha: Optional[date] = None

class LoncheraRead(BaseModel):
    id: int
    hijo_id: int
    fecha: date
    model_config = ConfigDict(from_attributes=True)
