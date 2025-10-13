from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Float
from app.db.database import Base

class Alimento(Base):
    __tablename__ = "alimentos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    kcal: Mapped[float] = mapped_column(Float, nullable=False)
    proteinas: Mapped[float] = mapped_column(Float, nullable=False)
    carbos: Mapped[float] = mapped_column(Float, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
