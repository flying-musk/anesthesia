"""
TTS (Text-to-Speech) API 端点
支持多语言文本转语音
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
import os
import tempfile
from datetime import datetime

router = APIRouter()


class TTSRequest(BaseModel):
    text: str
    language: str = "ja"  # ja, en, zh-TW, es, fr, ko
    slow: bool = False


@router.post("/generate")
async def generate_speech(request: TTSRequest):
    """
    生成语音文件

    支持的语言：
    - ja: 日本語
    - en: English
    - zh-TW: 繁體中文
    - es: Español
    - fr: Français
    - ko: 한국어
    """
    try:
        # 语言代码映射
        lang_map = {
            'ja': 'ja',
            'en': 'en',
            'zh-TW': 'zh-TW',
            'zh': 'zh-CN',
            'es': 'es',
            'fr': 'fr',
            'ko': 'ko',
        }

        gtts_lang = lang_map.get(request.language, 'ja')

        # 生成语音
        tts = gTTS(text=request.text, lang=gtts_lang, slow=request.slow)

        # 创建临时文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_{request.language}_{timestamp}.mp3"

        # 保存到临时目录
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)

        tts.save(file_path)

        return {
            "success": True,
            "message": "Speech generated successfully",
            "file_path": file_path,
            "filename": filename,
            "language": request.language,
            "text_length": len(request.text)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@router.post("/generate-file")
async def generate_speech_file(request: TTSRequest):
    """
    生成语音文件并直接返回文件
    """
    try:
        # 语言代码映射
        lang_map = {
            'ja': 'ja',
            'en': 'en',
            'zh-TW': 'zh-TW',
            'zh': 'zh-CN',
            'es': 'es',
            'fr': 'fr',
            'ko': 'ko',
        }

        gtts_lang = lang_map.get(request.language, 'ja')

        # 生成语音
        tts = gTTS(text=request.text, lang=gtts_lang, slow=request.slow)

        # 创建临时文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_{request.language}_{timestamp}.mp3"

        # 保存到临时目录
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)

        tts.save(file_path)

        # 返回文件
        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=filename
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@router.get("/languages")
async def get_supported_languages():
    """获取支持的语言列表"""
    return {
        "languages": {
            "ja": "日本語 (Japanese)",
            "en": "English",
            "zh-TW": "繁體中文 (Traditional Chinese)",
            "zh": "简体中文 (Simplified Chinese)",
            "es": "Español (Spanish)",
            "fr": "Français (French)",
            "ko": "한국어 (Korean)"
        }
    }


@router.post("/preview")
async def preview_text(request: TTSRequest):
    """
    预览文本信息（不生成音频）
    """
    return {
        "text": request.text,
        "language": request.language,
        "text_length": len(request.text),
        "estimated_duration_seconds": len(request.text) / 15,  # 大约估算
        "slow_mode": request.slow
    }
