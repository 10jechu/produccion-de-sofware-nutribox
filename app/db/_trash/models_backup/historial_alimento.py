from typing import Optional
from sqlmodel import SQLModel, Field

class HistorialAlimento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    alimento_id: int
    fecha_consumo: str
    observaciones: str
