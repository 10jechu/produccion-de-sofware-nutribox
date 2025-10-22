from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey

class Lonchera(SQLModel, table=True):
    __tablename__ = "loncheras"

    id: Optional[int] = Field(default=None, primary_key=True)
    hijo_id: int = Field(sa_column=Column(Integer, ForeignKey("hijos.id", ondelete="CASCADE"), nullable=False, index=True))
    fecha: str

    hijo: "Hijo" = Relationship(back_populates="loncheras")
    items: List["LoncheraAlimento"] = Relationship(back_populates="lonchera", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
