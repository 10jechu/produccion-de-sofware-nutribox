from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(30), unique=True, nullable=False)
    
class Membresia(Base):
    __tablename__ = "membresias"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20), unique=True, nullable=False)
    max_direcciones = Column(Integer, default=0, nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    activo = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    membresia_id = Column(Integer, ForeignKey("membresias.id"), nullable=False, index=True)
    
    rol = relationship("Rol", lazy="joined")
    membresia = relationship("Membresia", lazy="joined")
    hijos = relationship("Hijo", back_populates="padre", cascade="all, delete-orphan")
    direcciones = relationship("Direccion", cascade="all, delete-orphan")
    
    __table_args__ = (UniqueConstraint('email', name='uq_usuarios_email'),)

class Hijo(Base):
    __tablename__ = "hijos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    fecha_nacimiento = Column(String(10))
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    
    padre = relationship("Usuario", back_populates="hijos")
    loncheras = relationship("Lonchera", back_populates="hijo", cascade="all, delete-orphan")
