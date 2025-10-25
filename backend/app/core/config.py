"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List
from decouple import config


class Settings(BaseSettings):
    """Application settings"""

    # Basic settings
    PROJECT_NAME: str = "Anesthesia Pre-operative Information System"
    VERSION: str = "1.0.0"
    DEBUG: bool = config("DEBUG", default=True, cast=bool)
    HOST: str = config("HOST", default="0.0.0.0")
    PORT: int = config("PORT", default=8000, cast=int)

    # Database settings
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./anesthesia.db")

    # Security settings
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)

    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]
    ALLOWED_HOSTS: List[str] = ["*"]

    # AI service settings
    OPENAI_API_KEY: str = config("OPENAI_API_KEY", default="")
    USE_LOCAL_LLM: bool = config("USE_LOCAL_LLM", default=False, cast=bool)
    OLLAMA_URL: str = config("OLLAMA_URL", default="http://localhost:11434")
    OLLAMA_MODEL: str = config("OLLAMA_MODEL", default="qwen2.5:7b")

    # Redis settings
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379/0")

    # Logging settings
    LOG_LEVEL: str = config("LOG_LEVEL", default="INFO")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
