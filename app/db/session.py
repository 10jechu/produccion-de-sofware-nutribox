
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import DATABASE_URL, Base

# Engine y Session
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    # 1) Importa el registry de modelos (ejecuta todos los modules)
    import app.db.models  # NO BORRAR: fuerza el registro de todas las clases
    # 2) Crea tablas después de que todo está mapeado
    Base.metadata.create_all(bind=engine)

    """
    1) Importa dinámicamente todos los módulos en app.db.models (sin .bak / backup)
    2) Llama Base.metadata.create_all(bind=engine)
    """
    import importlib, pkgutil, pathlib
    import app.db.models as models_pkg

    pkg_path = pathlib.Path(models_pkg.__file__).parent
    for m in pkgutil.iter_modules([str(pkg_path)]):
        name = m.name
        # evita archivos de respaldo / privados
        if name.startswith("_") or name.endswith((".bak", "_backup")):
            continue
        importlib.import_module(f"app.db.models.{name}")
        print(f"[init_db] importado: app.db.models.{name}")

    # mapea TODO después de tener los modelos en el registry
    Base.metadata.create_all(bind=engine)
    print("[init_db] Base.metadata.create_all OK")
