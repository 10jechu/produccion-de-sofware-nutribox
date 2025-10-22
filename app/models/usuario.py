from __future__ import annotations
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    contrasena: str

    # 1:N Direccion
    direcciones: List["Direccion"] = Relationship(back_populates="usuario")

    # 1:N Hijo
    hijos: List["Hijo"] = Relationship(back_populates="usuario")
