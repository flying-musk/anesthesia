#!/usr/bin/env python3
"""
測試 Ollama 翻譯功能
"""

import os
import sys
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.services.medical_multilingual_service import medical_multilingual_service
from app.schemas.patient import LanguageEnum

async def test_ollama_translation():
    """測試 Ollama 翻譯功能"""
    print("=== 測試 Ollama 翻譯功能 ===")
    
    # 測試文本
    test_texts = [
        "Penicillin allergy",
        "Hypertension",
        "Blood pressure medication",
        "Appendectomy (2010)",
        "Father has diabetes"
    ]
    
    print("\n1. 測試中文翻譯:")
    for text in test_texts:
        try:
            translated = await medical_multilingual_service._translate_text(text, LanguageEnum.ZH)
            print(f"  原文: {text}")
            print(f"  中文: {translated}")
            print()
        except Exception as e:
            print(f"  翻譯失敗: {e}")
    
    print("\n2. 測試法文翻譯:")
    for text in test_texts:
        try:
            translated = await medical_multilingual_service._translate_text(text, LanguageEnum.FR)
            print(f"  原文: {text}")
            print(f"  法文: {translated}")
            print()
        except Exception as e:
            print(f"  翻譯失敗: {e}")
    
    print("\n=== 翻譯測試完成 ===")

if __name__ == "__main__":
    asyncio.run(test_ollama_translation())
