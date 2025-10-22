from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Inventario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    cantidad_total: int

    movimientos: List["InventarioMovimiento"] = Relationship(back_populates="inventario")
