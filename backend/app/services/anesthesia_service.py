"""
麻醉須知生成服務
"""

import openai
import json
import requests
from datetime import date
from typing import Dict, Any
from loguru import logger

from app.core.config import settings
from app.models.patient import Patient, MedicalHistory
from app.models.anesthesia import AnesthesiaGuideline
from app.schemas.anesthesia import GenerateGuidelineRequest


class AnesthesiaGuidelineService:
    """麻醉須知生成服務"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.ollama_url = settings.OLLAMA_URL
        self.ollama_model = settings.OLLAMA_MODEL
        self.use_local_llm = settings.USE_LOCAL_LLM
    
    async def generate_guideline(self, db, request: GenerateGuidelineRequest) -> AnesthesiaGuideline:
        """生成麻醉須知"""
        try:
            # 獲取患者資訊
            patient = db.query(Patient).filter(Patient.id == request.patient_id).first()
            if not patient:
                raise ValueError("患者不存在")
            
            # 準備患者醫療資訊
            patient_info = self._prepare_patient_info(patient)
            
            # 生成須知內容
            guideline_content = await self._generate_content(patient_info, request.dict())
            
            # 建立麻醉須知記錄
            guideline = AnesthesiaGuideline(
                patient_id=request.patient_id,
                surgery_name=request.surgery_name,
                anesthesia_type=request.anesthesia_type.value,
                surgery_date=request.surgery_date,
                surgeon_name=request.surgeon_name,
                anesthesiologist_name=request.anesthesiologist_name,
                **guideline_content,
                is_generated=True
            )
            
            db.add(guideline)
            db.commit()
            db.refresh(guideline)
            
            return guideline
            
        except Exception as e:
            logger.error(f"生成麻醉須知時發生錯誤: {str(e)}")
            db.rollback()
            raise
    
    def _prepare_patient_info(self, patient: Patient) -> Dict[str, Any]:
        """準備患者資訊"""
        info = {
            'basic_info': {
                'name': patient.full_name,
                'age': self._calculate_age(patient.date_of_birth),
                'gender': self._get_gender_display(patient.gender),
                'health_insurance_number': patient.health_insurance_number
            }
        }
        
        # 添加醫療病史
        from app.core.database import SessionLocal
        db = SessionLocal()
        medical_history = db.query(MedicalHistory).filter(MedicalHistory.patient_id == patient.id).first()
        if medical_history:
            info['medical_history'] = {
                'allergies': medical_history.allergies or '無',
                'chronic_conditions': medical_history.chronic_conditions or '無',
                'current_medications': medical_history.current_medications or '無',
                'previous_surgeries': medical_history.previous_surgeries or '無',
                'family_history': medical_history.family_history or '無'
            }
        else:
            info['medical_history'] = {
                'allergies': '無記錄',
                'chronic_conditions': '無記錄',
                'current_medications': '無記錄',
                'previous_surgeries': '無記錄',
                'family_history': '無記錄'
            }
        
        return info
    
    async def _generate_content(self, patient_info: Dict[str, Any], surgery_info: Dict[str, Any]) -> Dict[str, str]:
        """使用 AI 生成須知內容"""
        
        # 構建提示詞
        prompt = self._build_prompt(patient_info, surgery_info)
        
        try:
            if self.use_local_llm:
                # 使用本地LLM (Ollama)
                content = await self._generate_with_ollama(prompt)
            else:
                # 使用OpenAI
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "你是一位專業的麻醉科醫師，請根據患者資訊和手術資訊，生成詳細的麻醉前須知。請用繁體中文回答，內容要專業、易懂，適合患者閱讀。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                content = response.choices[0].message.content
            
            # 嘗試解析 JSON 格式的回應
            try:
                parsed_content = json.loads(content)
                return parsed_content
            except json.JSONDecodeError:
                # 如果不是 JSON 格式，使用預設模板
                return self._parse_text_response(content)
                
        except Exception as e:
            logger.error(f"AI 生成內容時發生錯誤: {str(e)}")
            # 使用預設模板
            return self._get_default_template(surgery_info['anesthesia_type'])
    
    def _build_prompt(self, patient_info: Dict[str, Any], surgery_info: Dict[str, Any]) -> str:
        """構建 AI 提示詞"""
        prompt = f"""
請根據以下患者資訊和手術資訊，生成詳細的麻醉前須知：

患者基本資訊：
- 姓名：{patient_info['basic_info']['name']}
- 年齡：{patient_info['basic_info']['age']}歲
- 性別：{patient_info['basic_info']['gender']}

醫療病史：
- 過敏史：{patient_info['medical_history']['allergies']}
- 慢性疾病：{patient_info['medical_history']['chronic_conditions']}
- 目前用藥：{patient_info['medical_history']['current_medications']}
- 手術史：{patient_info['medical_history']['previous_surgeries']}
- 家族病史：{patient_info['medical_history']['family_history']}

手術資訊：
- 手術名稱：{surgery_info['surgery_name']}
- 麻醉類型：{surgery_info['anesthesia_type']}
- 手術日期：{surgery_info['surgery_date']}

請生成以下內容，並以 JSON 格式回傳：

{{
    "anesthesia_type_info": "麻醉類型的詳細說明",
    "surgery_process": "手術過程的詳細描述",
    "expected_sensations": "患者可能感受到的各種感受",
    "potential_risks": "可能的風險和併發症",
    "pre_surgery_instructions": "術前準備事項",
    "fasting_instructions": "禁食禁水的具體時間和注意事項",
    "medication_instructions": "藥物停用的具體指示",
    "common_questions": "患者常問的問題和解答",
    "post_surgery_care": "術後照護注意事項"
}}

請確保內容專業、詳細且易懂。
        """
        return prompt
    
    def _parse_text_response(self, content: str) -> Dict[str, str]:
        """解析文字回應"""
        # 這裡可以實作文字解析邏輯
        # 暫時使用預設模板
        return self._get_default_template('general')
    
    def _get_default_template(self, anesthesia_type: str) -> Dict[str, str]:
        """獲取預設模板"""
        templates = {
            'general': {
                'anesthesia_type_info': '全身麻醉是讓您在手術過程中完全失去意識的麻醉方式。麻醉醫師會通過靜脈注射和氣體麻醉來確保您在手術期間完全無意識。',
                'surgery_process': '手術將在您完全無意識的狀態下進行。麻醉醫師會全程監控您的生命徵象，確保手術安全進行。',
                'expected_sensations': '您將不會感受到任何疼痛或不適。手術結束後，您會逐漸恢復意識，可能會感到輕微的頭暈或噁心。',
                'potential_risks': '可能包括：噁心、嘔吐、喉嚨痛、頭暈、肌肉疼痛等。嚴重併發症極為罕見，包括過敏反應、呼吸問題等。',
                'pre_surgery_instructions': '請按照醫師指示進行術前準備，包括禁食禁水、停用特定藥物等。',
                'fasting_instructions': '手術前8小時開始禁食，2小時前禁水。這是為了避免麻醉時發生嘔吐和吸入性肺炎的風險。',
                'medication_instructions': '請告知醫師您目前服用的所有藥物。某些藥物（如抗凝血劑）可能需要提前停用。',
                'common_questions': 'Q: 麻醉會不會有副作用？\nA: 大多數患者只會有輕微的副作用，如噁心、頭暈等，通常24小時內會消失。',
                'post_surgery_care': '術後請按照醫師指示進行照護，包括傷口護理、藥物服用、活動限制等。如有異常請立即就醫。'
            },
            'local': {
                'anesthesia_type_info': '局部麻醉是只麻醉手術部位，讓您在手術過程中保持清醒的麻醉方式。',
                'surgery_process': '手術過程中您會保持清醒，但手術部位不會感到疼痛。',
                'expected_sensations': '手術部位會有麻木感，但不會疼痛。您可能會感受到觸碰或壓力，但不會有痛感。',
                'potential_risks': '可能包括：注射部位疼痛、瘀血、感染等。嚴重併發症極為罕見。',
                'pre_surgery_instructions': '請按照醫師指示進行術前準備。',
                'fasting_instructions': '通常不需要禁食，但請按照醫師指示。',
                'medication_instructions': '請告知醫師您目前服用的所有藥物。',
                'common_questions': 'Q: 局部麻醉會不會痛？\nA: 注射時會有輕微刺痛，但很快就會麻木。',
                'post_surgery_care': '術後請按照醫師指示進行照護。麻醉效果通常會持續數小時。'
            }
        }
        return templates.get(anesthesia_type, templates['general'])
    
    def _calculate_age(self, date_of_birth: date) -> int:
        """計算年齡"""
        today = date.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    
    def _get_gender_display(self, gender: str) -> str:
        """取得性別顯示文字"""
        gender_map = {
            'M': '男性',
            'F': '女性',
            'O': '其他'
        }
        return gender_map.get(gender, '未知')
    
    async def _generate_with_ollama(self, prompt: str) -> str:
        """使用Ollama生成內容"""
        try:
            # 構建Ollama API請求
            payload = {
                "model": self.ollama_model,
                "prompt": f"你是一位專業的麻醉科醫師，請根據患者資訊和手術資訊，生成詳細的麻醉前須知。請用繁體中文回答，內容要專業、易懂，適合患者閱讀。\n\n{prompt}",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                logger.error(f"Ollama API 錯誤: {response.status_code}")
                raise Exception(f"Ollama API 錯誤: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            logger.error("無法連接到Ollama服務，請確保Ollama正在運行")
            raise Exception("無法連接到Ollama服務")
        except Exception as e:
            logger.error(f"Ollama生成內容時發生錯誤: {str(e)}")
            raise
