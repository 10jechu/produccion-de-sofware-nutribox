from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class InventarioMovimiento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str  # entrada o salida
    cantidad: int
    inventario_id: int = Field(foreign_key="inventario.id")

    inventario: "Inventario" = Relationship(back_populates="movimientos")
