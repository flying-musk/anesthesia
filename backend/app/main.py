"""
麻醉前須知生成系統 - FastAPI 主應用程式
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn
from decouple import config
from loguru import logger

from app.core.config import settings
from app.core.database import init_db
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理"""
    # 啟動時執行
    logger.info("啟動麻醉前須知生成系統...")
    await init_db()
    logger.info("資料庫初始化完成")
    yield
    # 關閉時執行
    logger.info("關閉麻醉前須知生成系統...")


# 建立 FastAPI 應用程式
app = FastAPI(
    title="麻醉前須知生成系統",
    description="基於 AI 的個人化麻醉前須知生成系統",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設定信任的主機
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# 包含 API 路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路徑"""
    return {
        "message": "麻醉前須知生成系統",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康檢查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
