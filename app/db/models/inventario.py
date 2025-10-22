from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .alimento import Alimento
from sqlalchemy.orm import relationship

class Inventario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ubicacion: str
    alimentos: List["Inventario_Movimiento"] = Relationship(back_populates="inventario")