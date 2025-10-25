"""
API v1 路由配置
"""

from fastapi import APIRouter
from app.api.v1.endpoints import patients, anesthesia, qa, tts, videos

api_router = APIRouter()

# 包含各端點路由
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(anesthesia.router, prefix="/anesthesia", tags=["anesthesia"])
api_router.include_router(qa.router, prefix="/qa", tags=["Q&A"])
api_router.include_router(tts.router, prefix="/tts", tags=["Text-to-Speech"])
api_router.include_router(videos.router, prefix="/videos", tags=["Videos"])
