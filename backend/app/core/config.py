"""
應用程式配置設定
"""

from pydantic_settings import BaseSettings
from typing import List
from decouple import config


class Settings(BaseSettings):
    """應用程式設定"""
    
    # 基本設定
    PROJECT_NAME: str = "麻醉前須知生成系統"
    VERSION: str = "1.0.0"
    DEBUG: bool = config("DEBUG", default=True, cast=bool)
    HOST: str = config("HOST", default="0.0.0.0")
    PORT: int = config("PORT", default=8000, cast=int)
    
    # 資料庫設定
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./anesthesia.db")
    
    # 安全設定
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    
    # CORS 設定
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # AI 服務設定
    OPENAI_API_KEY: str = config("OPENAI_API_KEY", default="")
    USE_LOCAL_LLM: bool = config("USE_LOCAL_LLM", default=False, cast=bool)
    OLLAMA_URL: str = config("OLLAMA_URL", default="http://localhost:11434")
    OLLAMA_MODEL: str = config("OLLAMA_MODEL", default="qwen2.5:7b")
    
    # Redis 設定
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379/0")
    
    # 日誌設定
    LOG_LEVEL: str = config("LOG_LEVEL", default="INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 建立全域設定實例
settings = Settings()
