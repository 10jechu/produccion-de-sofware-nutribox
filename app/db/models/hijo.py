from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.db.base_class import Base

class Hijo(Base):
    __tablename__ = "hijos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), index=True, nullable=False)
    
    # Relaciones
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="hijos")
    loncheras: Mapped[list["Lonchera"]] = relationship("Lonchera", back_populates="hijo", cascade="all, delete-orphan")
    restricciones: Mapped[list["Restriccion"]] = relationship("Restriccion", back_populates="hijo", cascade="all, delete-orphan")
