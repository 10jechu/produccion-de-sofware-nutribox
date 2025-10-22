from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey

class Direccion(SQLModel, table=True):
    __tablename__ = "direcciones"

    id: Optional[int] = Field(default=None, primary_key=True)
    alias: str
    calle: str
    ciudad: str
    usuario_id: int = Field(sa_column=Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True))

    usuario: "Usuario" = Relationship(back_populates="direcciones")
