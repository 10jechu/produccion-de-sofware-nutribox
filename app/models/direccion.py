from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Direccion(SQLModel, table=True):
    __tablename__ = "direccion"
    id: Optional[int] = Field(default=None, primary_key=True)
    calle: str
    ciudad: str
    pais: str
    usuario_id: int = Field(foreign_key="usuario.id")

    usuario: "Usuario" = Relationship(back_populates="direcciones")
