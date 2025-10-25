"""
视频管理 API 端点
支持视频上传、字幕生成、翻译等功能
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.video import Video, Subtitle, Translation
from app.utils.subtitle_generator import generate_webvtt, generate_srt
import os
import tempfile
import shutil

router = APIRouter()


class VideoResponse(BaseModel):
    id: int
    title: str
    file_path: str
    duration: Optional[float]
    language: str
    created_at: datetime

    class Config:
        from_attributes = True


class SubtitleRequest(BaseModel):
    video_id: int
    text: str
    start_time: float
    end_time: float
    language: str = "en"


class SubtitleResponse(BaseModel):
    id: int
    video_id: int
    start_time: float
    end_time: float
    text: str
    language: str

    class Config:
        from_attributes = True


class TranslationRequest(BaseModel):
    subtitle_id: int
    target_language: str
    text: str


@router.get("/list")
async def get_videos():
    """
    获取所有视频列表
    """
    try:
        # Mock data for now - later connect to database
        videos = [
            {
                "id": 1,
                "title": "麻酔の基本 - General Anesthesia Basics",
                "file_path": "/videos/anesthesia_basics.mp4",
                "duration": 300.5,
                "language": "ja",
                "created_at": datetime.now().isoformat(),
                "subtitle_count": 45,
                "translation_count": 3
            },
            {
                "id": 2,
                "title": "手術前の準備 - Pre-Surgery Preparation",
                "file_path": "/videos/pre_surgery.mp4",
                "duration": 420.0,
                "language": "ja",
                "created_at": datetime.now().isoformat(),
                "subtitle_count": 67,
                "translation_count": 2
            }
        ]

        return {
            "success": True,
            "videos": videos,
            "total": len(videos)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve videos: {str(e)}")


@router.post("/upload")
async def upload_video(
    title: str = Form(...),
    language: str = Form("ja"),
    file: UploadFile = File(...)
):
    """
    上传视频文件
    """
    try:
        # Create upload directory if not exists
        upload_dir = "/tmp/anesthesia_videos"
        os.makedirs(upload_dir, exist_ok=True)

        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"video_{timestamp}{file_extension}"
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # TODO: Save to database

        return {
            "success": True,
            "message": "Video uploaded successfully",
            "video": {
                "id": 999,  # Mock ID
                "title": title,
                "file_path": file_path,
                "language": language,
                "filename": filename
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/{video_id}/subtitles")
async def get_video_subtitles(video_id: int, language: Optional[str] = "ja"):
    """
    获取指定视频的字幕
    """
    try:
        # Mock subtitle data
        subtitles = [
            {
                "id": 1,
                "video_id": video_id,
                "start_time": 0.0,
                "end_time": 3.5,
                "text": "全身麻酔は非常に安全な医療処置です。",
                "language": "ja"
            },
            {
                "id": 2,
                "video_id": video_id,
                "start_time": 3.5,
                "end_time": 7.0,
                "text": "手術中は完全に意識がなくなり、痛みを感じることはありません。",
                "language": "ja"
            },
            {
                "id": 3,
                "video_id": video_id,
                "start_time": 7.0,
                "end_time": 11.0,
                "text": "麻酔科医が常に患者様の状態を監視しています。",
                "language": "ja"
            }
        ]

        return {
            "success": True,
            "video_id": video_id,
            "subtitles": subtitles,
            "total": len(subtitles)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve subtitles: {str(e)}")


@router.post("/subtitles")
async def create_subtitle(request: SubtitleRequest):
    """
    创建新字幕
    """
    try:
        # TODO: Save to database
        subtitle = {
            "id": 999,  # Mock ID
            "video_id": request.video_id,
            "start_time": request.start_time,
            "end_time": request.end_time,
            "text": request.text,
            "language": request.language
        }

        return {
            "success": True,
            "message": "Subtitle created successfully",
            "subtitle": subtitle
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create subtitle: {str(e)}")


@router.get("/{video_id}/subtitles/download")
async def download_subtitles(video_id: int, format: str = "vtt", language: str = "ja"):
    """
    下载字幕文件（VTT 或 SRT 格式）
    """
    try:
        # Mock subtitle data
        subtitles = [
            {"start_time": 0.0, "end_time": 3.5, "text": "全身麻酔は非常に安全な医療処置です。"},
            {"start_time": 3.5, "end_time": 7.0, "text": "手術中は完全に意識がなくなり、痛みを感じることはありません。"},
            {"start_time": 7.0, "end_time": 11.0, "text": "麻酔科医が常に患者様の状態を監視しています。"}
        ]

        # Generate subtitle file
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "vtt":
            filename = f"subtitles_{language}_{timestamp}.vtt"
            file_path = os.path.join(temp_dir, filename)
            generate_webvtt(subtitles, file_path)
            media_type = "text/vtt"
        else:  # srt
            filename = f"subtitles_{language}_{timestamp}.srt"
            file_path = os.path.join(temp_dir, filename)
            generate_srt(subtitles, file_path)
            media_type = "text/plain"

        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download subtitles: {str(e)}")


@router.post("/{video_id}/translate")
async def translate_subtitles(video_id: int, target_language: str):
    """
    翻译视频字幕到目标语言
    """
    try:
        # Mock translation
        translations = [
            {
                "id": 1,
                "subtitle_id": 1,
                "original_text": "全身麻酔は非常に安全な医療処置です。",
                "translated_text": "General anesthesia is a very safe medical procedure.",
                "target_language": target_language,
                "status": "completed"
            },
            {
                "id": 2,
                "subtitle_id": 2,
                "original_text": "手術中は完全に意識がなくなり、痛みを感じることはありません。",
                "translated_text": "During surgery, you will be completely unconscious and will not feel any pain.",
                "target_language": target_language,
                "status": "completed"
            }
        ]

        return {
            "success": True,
            "video_id": video_id,
            "target_language": target_language,
            "translations": translations,
            "total": len(translations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.get("/{video_id}/info")
async def get_video_info(video_id: int):
    """
    获取视频详细信息
    """
    try:
        # Mock video info
        video_info = {
            "id": video_id,
            "title": "麻酔の基本 - General Anesthesia Basics",
            "file_path": "/videos/anesthesia_basics.mp4",
            "duration": 300.5,
            "language": "ja",
            "created_at": datetime.now().isoformat(),
            "subtitle_languages": ["ja", "en", "zh-TW"],
            "total_subtitles": 45,
            "total_translations": 90,
            "statistics": {
                "views": 1234,
                "downloads": 56,
                "translations_requested": 23
            }
        }

        return {
            "success": True,
            "video": video_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve video info: {str(e)}")
