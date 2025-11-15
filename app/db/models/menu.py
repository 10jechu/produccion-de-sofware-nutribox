from sqlalchemy import Integer, String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

# Tabla de asociación muchos-a-muchos entre Menu y Alimento
menu_alimento = Table(
    'menu_alimento',
    Base.metadata,
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True),
    Column('alimento_id', Integer, ForeignKey('alimentos.id'), primary_key=True),
    Column('cantidad', Integer, default=1)
)

class Menu(Base):
    __tablename__ = "menus"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(200), default="")
    dia_semana: Mapped[str] = mapped_column(String(20))  # Lunes, Martes, etc.
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)  # Creador (Admin)
    
    # Relación muchos-a-muchos con alimentos (MANTENER ORIGINAL)
    alimentos = relationship("Alimento", secondary=menu_alimento, back_populates="menus")
    creador = relationship("Usuario")
