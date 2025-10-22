from sqlalchemy.orm import declarative_base

# SQLite local. Si usas otro motor, cambia la URL aquí.
DATABASE_URL = "sqlite:///./nutribox.db"

# Declarative Base compartida por TODOS los modelos
Base = declarative_base()
