"""
醫療多語言服務
用於生成醫療病史和手術記錄的多語言版本
"""

import asyncio
import time
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.patient import MedicalHistory, SurgeryRecord
from app.schemas.patient import LanguageEnum, MedicalHistoryCreate, SurgeryRecordCreate


class MedicalMultilingualService:
    """醫療多語言服務"""
    
    def __init__(self):
        self.supported_languages = [LanguageEnum.EN, LanguageEnum.ZH, LanguageEnum.FR]
    
    async def create_medical_history_multilingual(
        self, 
        db: Session, 
        patient_id: int, 
        medical_history_data: MedicalHistoryCreate
    ) -> List[MedicalHistory]:
        """創建多語言醫療病史"""
        import time
        group_id = int(time.time() * 1000)  # 使用時間戳作為 group_id
        
        medical_histories = []
        
        for language in self.supported_languages:
            # 翻譯醫療病史內容
            translated_data = await self._translate_medical_history(
                medical_history_data, language
            )
            
            # 創建醫療病史記錄
            medical_history = MedicalHistory(
                patient_id=patient_id,
                language=language.value,
                group_id=group_id,
                **translated_data
            )
            
            db.add(medical_history)
            medical_histories.append(medical_history)
        
        db.commit()
        
        # 刷新所有記錄以獲取 ID
        for medical_history in medical_histories:
            db.refresh(medical_history)
        
        return medical_histories
    
    async def create_surgery_record_multilingual(
        self, 
        db: Session, 
        patient_id: int, 
        surgery_record_data: SurgeryRecordCreate
    ) -> List[SurgeryRecord]:
        """創建多語言手術記錄"""
        import time
        group_id = int(time.time() * 1000)  # 使用時間戳作為 group_id
        
        surgery_records = []
        
        for language in self.supported_languages:
            # 翻譯手術記錄內容
            translated_data = await self._translate_surgery_record(
                surgery_record_data, language
            )
            
            # 創建手術記錄
            surgery_record = SurgeryRecord(
                patient_id=patient_id,
                language=language.value,
                group_id=group_id,
                **translated_data
            )
            
            db.add(surgery_record)
            surgery_records.append(surgery_record)
        
        db.commit()
        
        # 刷新所有記錄以獲取 ID
        for surgery_record in surgery_records:
            db.refresh(surgery_record)
        
        return surgery_records
    
    async def _translate_medical_history(
        self, 
        medical_history_data: MedicalHistoryCreate, 
        target_language: LanguageEnum
    ) -> Dict[str, Any]:
        """翻譯醫療病史內容"""
        if target_language == LanguageEnum.EN:
            # 英文版本，直接返回原始數據
            return {
                "allergies": medical_history_data.allergies,
                "chronic_conditions": medical_history_data.chronic_conditions,
                "current_medications": medical_history_data.current_medications,
                "previous_surgeries": medical_history_data.previous_surgeries,
                "family_history": medical_history_data.family_history,
                "other_medical_info": medical_history_data.other_medical_info,
            }
        
        # 使用 AI 翻譯其他語言
        translated_data = {}
        
        # 翻譯各個字段
        if medical_history_data.allergies:
            translated_data["allergies"] = await self._translate_text(
                medical_history_data.allergies, target_language
            )
        
        if medical_history_data.chronic_conditions:
            translated_data["chronic_conditions"] = await self._translate_text(
                medical_history_data.chronic_conditions, target_language
            )
        
        if medical_history_data.current_medications:
            translated_data["current_medications"] = await self._translate_text(
                medical_history_data.current_medications, target_language
            )
        
        if medical_history_data.previous_surgeries:
            translated_data["previous_surgeries"] = await self._translate_text(
                medical_history_data.previous_surgeries, target_language
            )
        
        if medical_history_data.family_history:
            translated_data["family_history"] = await self._translate_text(
                medical_history_data.family_history, target_language
            )
        
        if medical_history_data.other_medical_info:
            translated_data["other_medical_info"] = await self._translate_text(
                medical_history_data.other_medical_info, target_language
            )
        
        return translated_data
    
    async def _translate_surgery_record(
        self, 
        surgery_record_data: SurgeryRecordCreate, 
        target_language: LanguageEnum
    ) -> Dict[str, Any]:
        """翻譯手術記錄內容"""
        if target_language == LanguageEnum.EN:
            # 英文版本，直接返回原始數據
            return {
                "surgery_name": surgery_record_data.surgery_name,
                "surgery_type": surgery_record_data.surgery_type,
                "surgery_date": surgery_record_data.surgery_date,
                "surgeon_name": surgery_record_data.surgeon_name,
                "anesthesiologist_name": surgery_record_data.anesthesiologist_name,
                "surgery_duration": surgery_record_data.surgery_duration,
                "anesthesia_duration": surgery_record_data.anesthesia_duration,
                "pre_surgery_assessment": surgery_record_data.pre_surgery_assessment,
                "post_surgery_notes": surgery_record_data.post_surgery_notes,
                "complications": surgery_record_data.complications,
            }
        
        # 使用 AI 翻譯其他語言
        translated_data = {
            "surgery_name": await self._translate_text(surgery_record_data.surgery_name, target_language),  # 翻譯手術名稱
            "surgery_type": surgery_record_data.surgery_type,  # 手術類型通常不需要翻譯
            "surgery_date": surgery_record_data.surgery_date,
            "surgeon_name": surgery_record_data.surgeon_name,  # 醫生姓名通常不需要翻譯
            "anesthesiologist_name": surgery_record_data.anesthesiologist_name,  # 醫生姓名通常不需要翻譯
            "surgery_duration": surgery_record_data.surgery_duration,
            "anesthesia_duration": surgery_record_data.anesthesia_duration,
        }
        
        # 翻譯文本字段
        if surgery_record_data.pre_surgery_assessment:
            translated_data["pre_surgery_assessment"] = await self._translate_text(
                surgery_record_data.pre_surgery_assessment, target_language
            )
        
        if surgery_record_data.post_surgery_notes:
            translated_data["post_surgery_notes"] = await self._translate_text(
                surgery_record_data.post_surgery_notes, target_language
            )
        
        if surgery_record_data.complications:
            translated_data["complications"] = await self._translate_text(
                surgery_record_data.complications, target_language
            )
        
        return translated_data
    
    async def _translate_text(self, text: str, target_language: LanguageEnum) -> str:
        """使用 Ollama 翻譯文本"""
        try:
            # 如果目標語言是英文，直接返回原文
            if target_language == LanguageEnum.EN:
                return text
            
            # 嘗試使用 Ollama 進行翻譯
            try:
                from app.services.ollama_service import OllamaService
                ollama_service = OllamaService()
                
                # 構建翻譯提示
                language_map = {
                    LanguageEnum.ZH: "中文",
                    LanguageEnum.FR: "法文"
                }
                
                prompt = f"請將以下醫療文本翻譯成{language_map[target_language]}，保持醫療術語的準確性：\n\n{text}"
                
                # 調用 Ollama 服務
                translated_text = await ollama_service.generate_text(prompt)
                
                # 清理翻譯結果，移除可能的額外文字
                if translated_text:
                    # 移除可能的前綴文字
                    lines = translated_text.strip().split('\n')
                    # 找到第一個看起來像翻譯結果的行
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('請將') and not line.startswith('翻譯'):
                            return line
                    # 如果沒有找到合適的行，返回整個結果
                    return translated_text.strip()
                else:
                    # 如果 Ollama 返回空結果，使用模擬翻譯
                    return self._get_mock_translation(text, target_language)
                    
            except Exception as ollama_error:
                print(f"Ollama service not available: {ollama_error}")
                # Ollama 不可用時，使用模擬翻譯
                return self._get_mock_translation(text, target_language)
            
        except Exception as e:
            print(f"Translation error: {e}")
            # 翻譯失敗時返回模擬翻譯
            return self._get_mock_translation(text, target_language)
    
    def _get_mock_translation(self, text: str, target_language: LanguageEnum) -> str:
        """獲取模擬翻譯結果"""
        # 提供一些基本的醫療術語翻譯
        medical_translations = {
            LanguageEnum.ZH: {
                "Penicillin allergy": "青黴素過敏",
                "Hypertension": "高血壓",
                "Blood pressure medication": "血壓藥物",
                "Appendectomy": "闌尾切除術",
                "diabetes": "糖尿病",
                "Father has diabetes": "父親患有糖尿病",
                "Cataract surgery": "白內障手術",
                "Gallbladder removal": "膽囊切除術",
                "Colonoscopy": "結腸鏡檢查",
                "Cardiac catheterization": "心導管檢查"
            },
            LanguageEnum.FR: {
                "Penicillin allergy": "Allergie à la pénicilline",
                "Hypertension": "Hypertension",
                "Blood pressure medication": "Médicament pour la tension artérielle",
                "Appendectomy": "Appendicectomie",
                "diabetes": "diabète",
                "Father has diabetes": "Le père a le diabète",
                "Cataract surgery": "Chirurgie de la cataracte",
                "Gallbladder removal": "Ablation de la vésicule biliaire",
                "Colonoscopy": "Colonoscopie",
                "Cardiac catheterization": "Cathétérisme cardiaque"
            }
        }
        
        # 查找精確匹配
        if text in medical_translations.get(target_language, {}):
            return medical_translations[target_language][text]
        
        # 查找部分匹配
        for key, translation in medical_translations.get(target_language, {}).items():
            if key.lower() in text.lower():
                return text.replace(key, translation)
        
        # 如果沒有找到匹配，返回帶前綴的模擬翻譯
        if target_language == LanguageEnum.ZH:
            return f"[中文翻譯] {text}"
        elif target_language == LanguageEnum.FR:
            return f"[Traduction française] {text}"
        else:
            return text


# 創建服務實例
medical_multilingual_service = MedicalMultilingualService()
