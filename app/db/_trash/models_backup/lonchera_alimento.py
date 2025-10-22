from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .lonchera import Lonchera
from .alimento import Alimento

class Lonchera_Alimento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lonchera_id: Optional[int] = Field(foreign_key="lonchera.id")
    alimento_id: Optional[int] = Field(foreign_key="alimento.id")
    cantidad: int
    lonchera: Optional[Lonchera] = Relationship(back_populates="alimentos")
    alimento: Optional[Alimento] = Relationship(back_populates="lonchera_alimentos")
