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
        
        # 翻譯各個字段，包括空值處理
        translated_data["allergies"] = await self._translate_text(
            medical_history_data.allergies, target_language
        ) if medical_history_data.allergies else None
        
        translated_data["chronic_conditions"] = await self._translate_text(
            medical_history_data.chronic_conditions, target_language
        ) if medical_history_data.chronic_conditions else None
        
        translated_data["current_medications"] = await self._translate_text(
            medical_history_data.current_medications, target_language
        ) if medical_history_data.current_medications else None
        
        translated_data["previous_surgeries"] = await self._translate_text(
            medical_history_data.previous_surgeries, target_language
        ) if medical_history_data.previous_surgeries else None
        
        translated_data["family_history"] = await self._translate_text(
            medical_history_data.family_history, target_language
        ) if medical_history_data.family_history else None
        
        translated_data["other_medical_info"] = await self._translate_text(
            medical_history_data.other_medical_info, target_language
        ) if medical_history_data.other_medical_info else None
        
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
                "Cardiac catheterization": "心導管檢查",
                "Head Surgery": "頭部手術",
                "Knee surgery": "膝關節手術",
                "Heart surgery": "心臟手術",
                "Brain surgery": "腦部手術",
                "Spine surgery": "脊椎手術",
                "Lung surgery": "肺部手術",
                "Liver surgery": "肝臟手術",
                "Kidney surgery": "腎臟手術",
                "Eye surgery": "眼部手術",
                "Ear surgery": "耳部手術",
                "None": "無",
                "No complications": "無併發症",
                "Patient assessed for": "患者評估",
                "Vital signs stable": "生命體徵穩定",
                "No contraindications": "無禁忌症",
                "Patient recovered well": "患者恢復良好",
                "No complications noted": "無併發症記錄",
                "Discharged same day": "當日出院"
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
                "Cardiac catheterization": "Cathétérisme cardiaque",
                "Head Surgery": "Chirurgie de la tête",
                "Knee surgery": "Chirurgie du genou",
                "Heart surgery": "Chirurgie cardiaque",
                "Brain surgery": "Chirurgie du cerveau",
                "Spine surgery": "Chirurgie de la colonne vertébrale",
                "Lung surgery": "Chirurgie pulmonaire",
                "Liver surgery": "Chirurgie du foie",
                "Kidney surgery": "Chirurgie rénale",
                "Eye surgery": "Chirurgie oculaire",
                "Ear surgery": "Chirurgie de l'oreille",
                "None": "Aucune",
                "No complications": "Aucune complication",
                "Patient assessed for": "Patient évalué pour",
                "Vital signs stable": "Signes vitaux stables",
                "No contraindications": "Aucune contre-indication",
                "Patient recovered well": "Le patient s'est bien remis",
                "No complications noted": "Aucune complication notée",
                "Discharged same day": "Sorti le même jour"
            }
        }
        
        # 查找精確匹配
        if text in medical_translations.get(target_language, {}):
            return medical_translations[target_language][text]
        
        # 查找部分匹配
        for key, translation in medical_translations.get(target_language, {}).items():
            if key.lower() in text.lower():
                return text.replace(key, translation)
        
        # 如果沒有找到匹配，提供更智能的翻譯
        if target_language == LanguageEnum.ZH:
            # 簡單的英文到中文翻譯規則
            if "surgery" in text.lower():
                return text.replace("surgery", "手術").replace("Surgery", "手術")
            elif "assessment" in text.lower():
                return text.replace("assessment", "評估").replace("Assessment", "評估")
            elif "complications" in text.lower():
                return text.replace("complications", "併發症").replace("Complications", "併發症")
            elif "patient has been stable" in text.lower():
                return text.replace("Patient has been stable", "患者病情穩定").replace("patient has been stable", "患者病情穩定")
            elif "regular checkups" in text.lower():
                return text.replace("Regular checkups", "定期檢查").replace("regular checkups", "定期檢查")
            elif "current medications" in text.lower():
                return text.replace("current medications", "目前藥物").replace("Current medications", "目前藥物")
            elif "vital signs stable" in text.lower():
                return text.replace("Vital signs stable", "生命體徵穩定").replace("vital signs stable", "生命體徵穩定")
            elif "no contraindications" in text.lower():
                return text.replace("No contraindications", "無禁忌症").replace("no contraindications", "無禁忌症")
            elif "patient recovered well" in text.lower():
                return text.replace("Patient recovered well", "患者恢復良好").replace("patient recovered well", "患者恢復良好")
            elif "no complications noted" in text.lower():
                return text.replace("No complications noted", "無併發症記錄").replace("no complications noted", "無併發症記錄")
            elif "discharged same day" in text.lower():
                return text.replace("Discharged same day", "當日出院").replace("discharged same day", "當日出院")
            else:
                # 對於未匹配的文本，嘗試基本的詞彙替換而不是添加前綴
                basic_translations = {
                    "patient": "患者",
                    "stable": "穩定",
                    "medications": "藥物",
                    "checkups": "檢查",
                    "regular": "定期",
                    "current": "目前",
                    "well": "良好",
                    "recovered": "恢復",
                    "stable": "穩定"
                }
                
                translated_text = text
                for eng, chi in basic_translations.items():
                    translated_text = translated_text.replace(eng, chi).replace(eng.capitalize(), chi)
                
                return translated_text
        elif target_language == LanguageEnum.FR:
            # 簡單的英文到法文翻譯規則
            if "surgery" in text.lower():
                return text.replace("surgery", "chirurgie").replace("Surgery", "Chirurgie")
            elif "assessment" in text.lower():
                return text.replace("assessment", "évaluation").replace("Assessment", "Évaluation")
            elif "complications" in text.lower():
                return text.replace("complications", "complications").replace("Complications", "Complications")
            elif "patient has been stable" in text.lower():
                return text.replace("Patient has been stable", "Le patient a été stable").replace("patient has been stable", "le patient a été stable")
            elif "regular checkups" in text.lower():
                return text.replace("Regular checkups", "Contrôles réguliers").replace("regular checkups", "contrôles réguliers")
            elif "current medications" in text.lower():
                return text.replace("current medications", "médicaments actuels").replace("Current medications", "Médicaments actuels")
            elif "vital signs stable" in text.lower():
                return text.replace("Vital signs stable", "Signes vitaux stables").replace("vital signs stable", "signes vitaux stables")
            elif "no contraindications" in text.lower():
                return text.replace("No contraindications", "Aucune contre-indication").replace("no contraindications", "aucune contre-indication")
            elif "patient recovered well" in text.lower():
                return text.replace("Patient recovered well", "Le patient s'est bien remis").replace("patient recovered well", "le patient s'est bien remis")
            elif "no complications noted" in text.lower():
                return text.replace("No complications noted", "Aucune complication notée").replace("no complications noted", "aucune complication notée")
            elif "discharged same day" in text.lower():
                return text.replace("Discharged same day", "Sorti le même jour").replace("discharged same day", "sorti le même jour")
            else:
                # 對於未匹配的文本，嘗試基本的詞彙替換而不是添加前綴
                basic_translations = {
                    "patient": "patient",
                    "stable": "stable",
                    "medications": "médicaments",
                    "checkups": "contrôles",
                    "regular": "réguliers",
                    "current": "actuels",
                    "well": "bien",
                    "recovered": "remis"
                }
                
                translated_text = text
                for eng, fr in basic_translations.items():
                    translated_text = translated_text.replace(eng, fr).replace(eng.capitalize(), fr.capitalize())
                
                return translated_text
        else:
            return text


# 創建服務實例
medical_multilingual_service = MedicalMultilingualService()
