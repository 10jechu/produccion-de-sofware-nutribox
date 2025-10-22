from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .lonchera_alimento import LoncheraAlimento

class Alimento(SQLModel, table=True):
    __tablename__ = "alimento"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    calorias: int = 0

    loncheras: List["Lonchera"] = Relationship(
        back_populates="alimentos",
        link_model=LoncheraAlimento,
    )
