from __future__ import annotations
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from .link_hijo_restriccion import HijoRestriccionLink

class Restriccion(SQLModel, table=True):
    __tablename__ = "restriccion"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None

    # Lado inverso del M2M con Hijo
    hijos: List["Hijo"] = Relationship(
        back_populates="restricciones",
        link_model=HijoRestriccionLink,
    )
