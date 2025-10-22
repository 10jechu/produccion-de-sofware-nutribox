from typing import List
from sqlmodel import Relationship

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Hijo(Base):
    __tablename__ = "hijos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)

    # FK a usuarios.id (tabla 'usuarios')
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relación inversa con Usuario
    usuario: "Usuario" = Relationship(back_populates="hijos")
    usuario: "Usuario" = Relationship(back_populates="hijos")
    loncheras: List["Lonchera"] = Relationship(back_populates="hijo", sa_relationship_kwargs={"cascade":"all, delete-orphan"})