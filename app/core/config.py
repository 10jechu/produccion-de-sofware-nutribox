# app/core/config.py
from pydantic_settings import BaseSettings  # <- antes estaba en pydantic

class Settings(BaseSettings):
    APP_NAME: str = "NutriBox API"
    ENV: str = "dev"
    DATABASE_URL: str = "sqlite:///./nutribox.db"  # local; luego PostgreSQL en Azure

    class Config:
        env_file = ".env"

settings = Settings()
