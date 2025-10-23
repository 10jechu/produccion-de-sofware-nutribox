from sqlmodel import SQLModel
from app.db.session import get_session
from app import models  # registra metadatos

def init_db():
    SQLModel.metadata.create_all(engine)
