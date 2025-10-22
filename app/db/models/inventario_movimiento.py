from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Inventario_Movimiento(SQLModel, table=True):
    __tablename__ = "inventario_movimiento"
    id: Optional[int] = Field(default=None, primary_key=True)
    inventario_id: int = Field(foreign_key="inventario.id", index=True)
    tipo: str  # "entrada" | "salida"
    cantidad: int
    fecha: datetime = Field(default_factory=datetime.utcnow)

    inventario: "Inventario" = Relationship(back_populates="movimientos")
