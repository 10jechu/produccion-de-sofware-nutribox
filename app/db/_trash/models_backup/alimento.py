from typing import Optional
from sqlmodel import SQLModel, Field

class Alimento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    calorias: int
