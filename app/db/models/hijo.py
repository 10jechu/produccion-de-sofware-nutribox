from __future__ import annotations
from typing import List
from sqlmodel import SQLModel, Field, Relationship
from .link_hijo_restriccion import HijoRestriccionLink

class Hijo(SQLModel, table=True):
    __tablename__ = "hijos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha_nacimiento: str  # cambia a date si luego quieres

    # M2M hacia Restriccion (anotación + Relationship() solo con kwargs)
    restricciones: List["Restriccion"] = Relationship(
        back_populates="hijos",
        link_model=HijoRestriccionLink,
    )

    # 1:N con Lonchera
    loncheras: List["Lonchera"] = Relationship(back_populates="hijo")
