from sqlmodel import Relationship
from sqlalchemy import ForeignKey
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .usuario import Usuario
from sqlalchemy.orm import relationship

class Direccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    calle: str
    ciudad: str
    usuario_id: Optional[int] = Field(foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="direccions")
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False, index=True)
    usuario = relationship('Usuario', back_populates='direcciones')