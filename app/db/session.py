from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base_class import Base

DATABASE_URL = "sqlite:///./nutribox.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# IMPORTAR TODOS LOS MODELOS para que SQLAlchemy los vea
from app.db.models import (
    Rol, Membresia, Usuario, Hijo, Alimento, 
    Lonchera, LoncheraAlimento, Direccion, Restriccion
)

def init_db():
    """Crea todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
