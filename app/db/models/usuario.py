from typing import List
from sqlmodel import Relationship

from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    # email único (usa 'email' para alinearlo con auth)
    email = Column(String(255), unique=True, index=True, nullable=False)

    # password hasheado
    hash_password = Column(String(255), nullable=False)

    # estado y timestamps
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # relaciones
    hijos: List["Hijo"] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade":"all, delete-orphan"})
    __table_args__ = (
        UniqueConstraint('email', name='uq_usuarios_email'),
    )
    hijos: List["Hijo"] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade":"all, delete-orphan"})
    direcciones: List["Direccion"] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade":"all, delete-orphan"})