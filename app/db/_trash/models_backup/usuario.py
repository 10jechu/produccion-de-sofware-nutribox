from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class UsuarioBase(SQLModel):
    nombre: str
    correo: str
    contrasena: str

class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hijos: List["Hijo"] = Relationship(back_populates="padre")
    direccions: List["Direccion"] = Relationship(back_populates="usuario")

class UsuarioCreate(UsuarioBase):
    nombre: str
    correo: str
    contrasena: str

class UsuarioRead(UsuarioBase):
    id: int
