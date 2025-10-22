from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

DATABASE_URL = "sqlite:///./nutribox.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# IMPORTA TODOS LOS MODELOS para que SQLAlchemy vea las tablas
from app.db.models import *  # noqa

def init_db():
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
