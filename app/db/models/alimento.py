from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Float
from app.db.database import Base

class Alimento(Base):
    __tablename__ = "alimentos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    kcal: Mapped[float] = mapped_column(Float, nullable=False)
    proteinas: Mapped[float] = mapped_column(Float, nullable=False)
    carbos: Mapped[float] = mapped_column(Float, nullable=False)
    costo: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Nueva relación con menus (MANTENER CONSISTENTE)
    menus = relationship("Menu", secondary="menu_alimento", back_populates="alimentos")
