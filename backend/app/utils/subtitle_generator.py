"""
字幕生成器
生成WebVTT/SRT格式的字幕文件
"""

from typing import List, Dict
from sqlalchemy.orm import Session


def generate_webvtt(subtitles: List[Dict]) -> str:
    """
    生成WebVTT格式字幕

    Args:
        subtitles: 字幕列表，每项包含 start_time, end_time, text

    Returns:
        WebVTT格式字符串
    """
    vtt = "WEBVTT\n\n"

    for idx, sub in enumerate(subtitles, 1):
        start = format_webvtt_time(sub['start_time'])
        end = format_webvtt_time(sub['end_time'])
        text = sub['text']

        vtt += f"{idx}\n"
        vtt += f"{start} --> {end}\n"
        vtt += f"{text}\n\n"

    return vtt


def generate_srt(subtitles: List[Dict]) -> str:
    """
    生成SRT格式字幕

    Args:
        subtitles: 字幕列表

    Returns:
        SRT格式字符串
    """
    srt = ""

    for idx, sub in enumerate(subtitles, 1):
        start = format_srt_time(sub['start_time'])
        end = format_srt_time(sub['end_time'])
        text = sub['text']

        srt += f"{idx}\n"
        srt += f"{start} --> {end}\n"
        srt += f"{text}\n\n"

    return srt


def format_webvtt_time(seconds: float) -> str:
    """
    格式化时间为WebVTT格式: HH:MM:SS.mmm

    Args:
        seconds: 秒数

    Returns:
        格式化的时间字符串
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def format_srt_time(seconds: float) -> str:
    """
    格式化时间为SRT格式: HH:MM:SS,mmm

    Args:
        seconds: 秒数

    Returns:
        格式化的时间字符串
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def subtitles_from_db(db: Session, video_id: int, language: str) -> List[Dict]:
    """
    从数据库读取字幕并准备生成

    Args:
        db: 数据库会话
        video_id: 视频ID
        language: 语言代码

    Returns:
        字幕列表
    """
    from app.models.video import Subtitle, Translation

    # 获取字幕
    subtitles = db.query(Subtitle).filter(
        Subtitle.video_id == video_id
    ).order_by(Subtitle.sequence).all()

    result = []

    for subtitle in subtitles:
        # 如果是原始语言，直接使用原文
        if language == 'en' or language == subtitle.language:
            text = subtitle.text
        else:
            # 获取翻译
            translation = db.query(Translation).filter(
                Translation.subtitle_id == subtitle.id,
                Translation.language == language
            ).order_by(Translation.version.desc()).first()

            if translation:
                text = translation.translated_text
            else:
                # 没有翻译，使用原文
                text = subtitle.text

        result.append({
            'start_time': subtitle.start_time,
            'end_time': subtitle.end_time,
            'text': text
        })

    return result
