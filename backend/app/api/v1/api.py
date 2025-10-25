"""
API v1 路由配置
"""

from fastapi import APIRouter
from app.api.v1.endpoints import patients, anesthesia

api_router = APIRouter()

# 包含各端點路由
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(anesthesia.router, prefix="/anesthesia", tags=["anesthesia"])
