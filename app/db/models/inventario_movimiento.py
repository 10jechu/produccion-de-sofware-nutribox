from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .inventario import Inventario
from .alimento import Alimento
from sqlalchemy.orm import relationship

class Inventario_Movimiento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cantidad: int
    inventario_id: Optional[int] = Field(foreign_key="inventario.id")
    alimento_id: Optional[int] = Field(foreign_key="alimento.id")
    inventario: Optional[Inventario] = Relationship(back_populates="alimentos")
    alimento: Optional[Alimento] = Relationship(back_populates="inventario_movimientos")