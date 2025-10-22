from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Rol(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    usuarios = relationship("Usuario", back_populates="rol")

class Membresia(Base):
    __tablename__ = "membresias"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20), unique=True, nullable=False)  # Free, Premium
    max_direcciones = Column(Integer, default=1)
    descripcion = Column(String(200), nullable=True)
    
    # Relationships
    usuarios = relationship("Usuario", back_populates="membresia")

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Foreign Keys
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    membresia_id = Column(Integer, ForeignKey("membresias.id"), nullable=False)
    
    # Relationships
    rol = relationship("Rol", back_populates="usuarios")
    membresia = relationship("Membresia", back_populates="usuarios")
    hijos = relationship("Hijo", back_populates="usuario", cascade="all, delete-orphan")
    direcciones = relationship("Direccion", back_populates="usuario", cascade="all, delete-orphan")

class Hijo(Base):
    __tablename__ = "hijos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    fecha_nacimiento = Column(String(10), nullable=False)  # YYYY-MM-DD
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    
    # Relationships
    usuario = relationship("Usuario", back_populates="hijos")
    loncheras = relationship("Lonchera", back_populates="hijo", cascade="all, delete-orphan")
    restricciones = relationship("Restriccion", back_populates="hijo", cascade="all, delete-orphan")
