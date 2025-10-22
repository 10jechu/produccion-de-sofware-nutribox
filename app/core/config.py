from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NutriBox API"
    VERSION: str = "2.1.0"
    DATABASE_URL: str = "sqlite:///./nutribox.db"
    ALLOWED_ORIGINS: list[str] = ["*"]
    SECRET_KEY: str = "dev-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24

    class Config:
        env_file = ".env"

settings = Settings()
