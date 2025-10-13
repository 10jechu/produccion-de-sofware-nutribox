from datetime import date
from sqlalchemy import Integer, String, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Lonchera(Base):
    __tablename__ = "loncheras"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hijo_id: Mapped[int] = mapped_column(ForeignKey("hijos.id"), index=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="Borrador")  # Borrador/Asignada/...

class LoncheraAlimento(Base):
    __tablename__ = "lonchera_alimento"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lonchera_id: Mapped[int] = mapped_column(ForeignKey("loncheras.id"), index=True)
    alimento_id: Mapped[int] = mapped_column(ForeignKey("alimentos.id"), index=True)
    cantidad: Mapped[float] = mapped_column(Float, default=1.0)  # porciones
    __table_args__ = (UniqueConstraint("lonchera_id", "alimento_id", name="uq_lonchera_alimento"),)
