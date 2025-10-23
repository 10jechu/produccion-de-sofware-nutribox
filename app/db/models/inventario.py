from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Inventario(SQLModel, table=True):
    __tablename__ = "inventario"
    id: Optional[int] = Field(default=None, primary_key=True)
    alimento_id: int = Field(foreign_key="alimento.id", index=True)
    cantidad: int = 0
    usuario_id: int = Field(foreign_key="usuario.id", index=True)

    alimento: "Alimento" = Relationship()
    usuario: "Usuario" = Relationship()
    movimientos: List["Inventario_Movimiento"] = Relationship(
        back_populates="inventario",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
