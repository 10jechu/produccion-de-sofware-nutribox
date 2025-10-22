from typing import List
from sqlmodel import SQLModel, Field, Relationship

class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    contrasena: str

    # 1:N con Direccion
    direcciones: List["Direccion"] = Relationship(back_populates="usuario")
