"""
视频字幕系统数据模型
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Video(Base):
    """视频表"""
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    file_path = Column(String(500), nullable=False)
    duration = Column(Float, nullable=True)  # 视频时长（秒）
    description = Column(Text, nullable=True)
    original_language = Column(String(10), default='en')
    available_audio_languages = Column(Text, nullable=True)  # 逗号分隔的音频语言列表
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    subtitles = relationship("Subtitle", back_populates="video", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Video(id={self.id}, title='{self.title}')>"


class Subtitle(Base):
    """字幕段落表"""
    __tablename__ = "subtitles"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    sequence = Column(Integer, nullable=False)  # 字幕序号
    start_time = Column(Float, nullable=False)  # 开始时间（秒）
    end_time = Column(Float, nullable=False)    # 结束时间（秒）
    text = Column(Text, nullable=False)         # 原始文本
    language = Column(String(10), default='en')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    video = relationship("Video", back_populates="subtitles")
    translations = relationship("Translation", back_populates="subtitle", cascade="all, delete-orphan")

    # 确保同一视频的字幕序号唯一
    __table_args__ = (
        UniqueConstraint('video_id', 'sequence', name='uix_video_sequence'),
    )

    def __repr__(self):
        return f"<Subtitle(id={self.id}, seq={self.sequence}, time={self.start_time}-{self.end_time})>"


class Translation(Base):
    """翻译表"""
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    subtitle_id = Column(Integer, ForeignKey("subtitles.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(10), nullable=False)  # 'zh-TW', 'es', 'ja', 'fr' etc.
    translated_text = Column(Text, nullable=False)
    status = Column(String(20), default='draft')   # draft, reviewed, approved
    reviewed_by = Column(String(100), nullable=True)  # 审核人
    reviewed_at = Column(DateTime(timezone=True), nullable=True)  # 审核时间
    version = Column(Integer, default=1)           # 版本号
    notes = Column(Text, nullable=True)            # 审核备注
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    subtitle = relationship("Subtitle", back_populates="translations")

    # 确保同一字幕的同一语言同一版本唯一
    __table_args__ = (
        UniqueConstraint('subtitle_id', 'language', 'version', name='uix_subtitle_language_version'),
    )

    def __repr__(self):
        return f"<Translation(id={self.id}, lang={self.language}, status={self.status})>"


class Terminology(Base):
    """医学术语词典表"""
    __tablename__ = "terminology"

    id = Column(Integer, primary_key=True, index=True)
    term_en = Column(String(200), nullable=False, unique=True, index=True)  # 英文术语
    term_zh = Column(String(200), nullable=True)  # 中文翻译
    term_es = Column(String(200), nullable=True)  # 西班牙文翻译
    term_ja = Column(String(200), nullable=True)  # 日文翻译
    term_fr = Column(String(200), nullable=True)  # 法文翻译
    category = Column(String(50), nullable=True)  # 分类（如：药物、程序、症状）
    definition = Column(Text, nullable=True)      # 术语定义
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Terminology(en='{self.term_en}', zh='{self.term_zh}')>"
