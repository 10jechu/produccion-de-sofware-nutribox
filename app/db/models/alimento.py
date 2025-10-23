from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class Alimento(Base):
    __tablename__ = "alimentos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # Información nutricional (por unidad)
    calorias: Mapped[float] = mapped_column(Float, nullable=False)
    proteinas: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    grasas: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    carbohidratos: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    # Unidad de medida
    unidad: Mapped[str] = mapped_column(String(20), default="unidad", nullable=False)  # unidad, g, ml, porcion
    
    # Estado (para soft delete)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
