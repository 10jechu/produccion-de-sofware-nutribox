from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "NutriBox API"
    debug: bool = True
    
    # Configuración de base de datos
    DATABASE_URL: str = "sqlite:///./nutribox.db"
    
    # Configuración JWT
    SECRET_KEY: str = "tu-clave-secreta-aqui-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
