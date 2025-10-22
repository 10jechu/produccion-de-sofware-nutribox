from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # General
    ENV: str = "development"
    PROJECT_NAME: str = "NutriBox API"
    VERSION: str = "2.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./nutribox.db"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
