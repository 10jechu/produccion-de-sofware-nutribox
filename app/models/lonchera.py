from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Lonchera(SQLModel, table=True):
    __tablename__ = "lonchera"
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: str
    hijo_id: int = Field(foreign_key="hijos.id")

    hijo: "Hijo" = Relationship(back_populates="loncheras")

    alimentos: List["Alimento"] = Relationship(
        back_populates="loncheras",
        link_model="app.models.lonchera_alimento.LoncheraAlimento",  # referencia plena evita import circular
    )
