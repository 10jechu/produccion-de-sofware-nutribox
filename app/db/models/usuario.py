from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo", nullable=False)  # activo, inactivo, suspendido
    
    # Foreign Keys
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False, index=True)
    membresia_id: Mapped[int] = mapped_column(ForeignKey("membresias.id"), nullable=False, index=True)
    
    # Relaciones
    rol: Mapped["Rol"] = relationship("Rol", back_populates="usuarios")
    membresia: Mapped["Membresia"] = relationship("Membresia", back_populates="usuarios")
    hijos: Mapped[list["Hijo"]] = relationship("Hijo", back_populates="usuario", cascade="all, delete-orphan")
    direcciones: Mapped[list["Direccion"]] = relationship("Direccion", back_populates="usuario", cascade="all, delete-orphan")
