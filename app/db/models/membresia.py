from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Membresia(Base):
    __tablename__ = "membresias"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tipo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)  # Basico, Estandar, Premium
    max_direcciones: Mapped[int] = mapped_column(Integer, default=1)
    precio: Mapped[float] = mapped_column(Float, nullable=True)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Relación con usuarios
    usuarios: Mapped[list["Usuario"]] = relationship("Usuario", back_populates="membresia")
