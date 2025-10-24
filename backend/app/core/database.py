"""
資料庫設定和連接管理
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 建立資料庫引擎
# SQLite 不需要連接池設定
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG
    )

# 建立 SessionLocal 類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立 Base 類別
Base = declarative_base()


def get_db():
    """取得資料庫會話"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """初始化資料庫"""
    # 建立所有表格
    Base.metadata.create_all(bind=engine)
