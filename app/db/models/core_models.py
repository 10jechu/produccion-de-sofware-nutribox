from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, Boolean, ForeignKey, Integer
from app.db.database import Base

class Rol(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

class Membresia(Base):
    __tablename__ = "membresias"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tipo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)  # Basico/Estandar/Premium
    max_direcciones: Mapped[int] = mapped_column(Integer, default=0)

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    membresia_id: Mapped[int] = mapped_column(ForeignKey("membresias.id"))

    rol = relationship("Rol")
    membresia = relationship("Membresia")
    hijos = relationship("Hijo", back_populates="padre", cascade="all, delete-orphan")

class Hijo(Base):
    __tablename__ = "hijos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)

    padre = relationship("Usuario", back_populates="hijos")
