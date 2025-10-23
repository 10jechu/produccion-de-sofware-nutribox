from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base_class import Base

DATABASE_URL = "sqlite:///./nutribox.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    import app.db.models
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
