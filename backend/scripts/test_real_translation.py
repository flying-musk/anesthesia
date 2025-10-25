#!/usr/bin/env python3
"""
測試真實 AI 翻譯功能
"""

import os
import sys
import asyncio

# Add the parent directory to the Python path to allow imports from 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.services.medical_multilingual_service import medical_multilingual_service
from app.schemas.patient import LanguageEnum

async def test_real_translation():
    """測試真實的 AI 翻譯功能"""
    print("=== 測試真實 AI 翻譯功能 ===")
    
    # 測試文本
    test_texts = [
        "Penicillin allergy",
        "Hypertension",
        "Blood pressure medication",
        "Appendectomy (2010)",
        "Father has diabetes",
        "Patient assessed for cataract surgery. Vital signs stable.",
        "Patient recovered well. No complications noted."
    ]
    
    for text in test_texts:
        print(f"\n原文: {text}")
        
        # 測試中文翻譯
        try:
            zh_translation = await medical_multilingual_service._translate_text(text, LanguageEnum.ZH)
            print(f"中文翻譯: {zh_translation}")
        except Exception as e:
            print(f"中文翻譯失敗: {e}")
        
        # 測試法文翻譯
        try:
            fr_translation = await medical_multilingual_service._translate_text(text, LanguageEnum.FR)
            print(f"法文翻譯: {fr_translation}")
        except Exception as e:
            print(f"法文翻譯失敗: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_real_translation())
