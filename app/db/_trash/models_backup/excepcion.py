from typing import Optional
from sqlmodel import SQLModel, Field
from .restriccion import Restriccion

class Excepcion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    restriccion_id: Optional[int] = Field(foreign_key="restriccion.id")
    restriccion: Optional[Restriccion] = Relationship(back_populates="excepcions")
