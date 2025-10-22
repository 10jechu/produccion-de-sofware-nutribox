from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    hash_password: str

    hijos: List["Hijo"] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    direcciones: List["Direccion"] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
