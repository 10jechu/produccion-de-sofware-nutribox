from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey

class Hijo(SQLModel, table=True):
    __tablename__ = "hijos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    fecha_nacimiento: str  # puedes cambiar a date más adelante
    usuario_id: int = Field(sa_column=Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True))

    usuario: "Usuario" = Relationship(back_populates="hijos")
    loncheras: List["Lonchera"] = Relationship(back_populates="hijo", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
