from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .alimento import Alimento
from sqlalchemy.orm import relationship

class Historial_Alimento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: str
    alimento_id: Optional[int] = Field(foreign_key="alimento.id")
    alimento: Optional[Alimento] = Relationship(back_populates="historiales")