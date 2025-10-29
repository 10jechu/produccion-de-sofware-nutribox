# app/db/models/menu.py
from sqlalchemy import Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class MenuPredeterminado(Base):
    __tablename__ = "menus_predeterminados"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Relación con los items que componen este menú
    items = relationship("MenuPredeterminadoItem", back_populates="menu", cascade="all, delete-orphan")

class MenuPredeterminadoItem(Base):
    __tablename__ = "menu_predeterminado_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    menu_id: Mapped[int] = mapped_column(ForeignKey("menus_predeterminados.id"), index=True)
    alimento_id: Mapped[int] = mapped_column(ForeignKey("alimentos.id"), index=True)
    cantidad: Mapped[float] = mapped_column(Float, default=1.0)

    menu = relationship("MenuPredeterminado", back_populates="items")
    # Opcional: Relación para acceder directamente al alimento desde el item
    alimento = relationship("Alimento")

    __table_args__ = (UniqueConstraint("menu_id", "alimento_id", name="uq_menu_predeterminado_item"),)