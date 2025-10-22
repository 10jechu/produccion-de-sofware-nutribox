from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class Alimento(Base):
    __tablename__ = "alimentos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)
    calorias: Mapped[float] = mapped_column(Float, nullable=False)
    proteinas: Mapped[float] = mapped_column(Float, default=0.0)
    grasas: Mapped[float] = mapped_column(Float, default=0.0)
    carbohidratos: Mapped[float] = mapped_column(Float, default=0.0)
    unidad: Mapped[str] = mapped_column(String(20), default="unidad")  # unidad, g, ml, porcion
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
