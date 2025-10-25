"""
Anesthesia Guideline Generation Service
"""

import openai
import json
import requests
from datetime import date
from typing import Dict, Any, List
from loguru import logger

from app.core.config import settings
from app.models.patient import Patient, MedicalHistory
from app.models.anesthesia import AnesthesiaGuideline
from app.schemas.anesthesia import GenerateGuidelineRequest, LanguageEnum
from app.services.medical_multilingual_service import medical_multilingual_service


class AnesthesiaGuidelineService:
    """Service for generating anesthesia guidelines."""

    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.ollama_url = settings.OLLAMA_URL
        self.ollama_model = settings.OLLAMA_MODEL
        self.use_local_llm = settings.USE_LOCAL_LLM

    async def generate_guideline_multilingual(self, db, request: GenerateGuidelineRequest) -> List[AnesthesiaGuideline]:
        """Generate anesthesia guideline in multiple languages (always generates all 3 languages)."""
        try:
            # Get patient information
            patient = db.query(Patient).filter(Patient.id == request.patient_id).first()
            if not patient:
                raise ValueError("Patient not found")

            # Prepare patient medical information
            patient_info = self._prepare_patient_info(patient)

            # Generate for all supported languages from the multilingual service
            all_languages = medical_multilingual_service.supported_languages
            guidelines = []

            # Generate a unique group_id for this set of guidelines
            import time
            group_id = int(time.time() * 1000)  # Use timestamp as group_id

            # Generate guidelines for each language
            for language in all_languages:
                # Generate guideline content for this language
                guideline_content = await self._generate_content_for_language(
                    patient_info, request.dict(), language
                )

                # Create anesthesia guideline record
                guideline = AnesthesiaGuideline(
                    patient_id=request.patient_id,
                    surgery_name=request.surgery_name,
                    anesthesia_type=request.anesthesia_type.value,
                    surgery_date=request.surgery_date,
                    surgeon_name=request.surgeon_name,
                    anesthesiologist_name=request.anesthesiologist_name,
                    language=language.value,
                    group_id=group_id,
                    **guideline_content,
                    is_generated=True
                )

                db.add(guideline)
                guidelines.append(guideline)

            db.commit()

            # Refresh all guidelines
            for guideline in guidelines:
                db.refresh(guideline)

            # Return only the requested language if specified, otherwise return all
            if request.return_language:
                return [g for g in guidelines if g.language == request.return_language.value]
            else:
                return guidelines

        except Exception as e:
            logger.error(f"Error generating anesthesia guideline: {str(e)}")
            db.rollback()
            raise

    async def generate_guideline(self, db, request: GenerateGuidelineRequest) -> AnesthesiaGuideline:
        """Generate anesthesia guideline (legacy method for single language)."""
        try:
            # Get patient information
            patient = db.query(Patient).filter(Patient.id == request.patient_id).first()
            if not patient:
                raise ValueError("Patient not found")

            # Prepare patient medical information
            patient_info = self._prepare_patient_info(patient)

            # Generate guideline content (default to English)
            guideline_content = await self._generate_content_for_language(
                patient_info, request.dict(), LanguageEnum.EN
            )

            # Create anesthesia guideline record
            guideline = AnesthesiaGuideline(
                patient_id=request.patient_id,
                surgery_name=request.surgery_name,
                anesthesia_type=request.anesthesia_type.value,
                surgery_date=request.surgery_date,
                surgeon_name=request.surgeon_name,
                anesthesiologist_name=request.anesthesiologist_name,
                language=LanguageEnum.EN.value,
                **guideline_content,
                is_generated=True
            )

            db.add(guideline)
            db.commit()
            db.refresh(guideline)

            return guideline

        except Exception as e:
            logger.error(f"Error generating anesthesia guideline: {str(e)}")
            db.rollback()
            raise

    def _prepare_patient_info(self, patient: Patient) -> Dict[str, Any]:
        """Prepare patient information."""
        info = {
            'basic_info': {
                'name': patient.full_name,
                'age': self._calculate_age(patient.date_of_birth),
                'gender': self._get_gender_display(patient.gender),
                'health_insurance_number': patient.health_insurance_number
            }
        }

        # Add medical history
        from app.core.database import SessionLocal
        db = SessionLocal()
        try:
            medical_history = db.query(MedicalHistory).filter(MedicalHistory.patient_id == patient.id).first()
            if medical_history:
                info['medical_history'] = {
                    'allergies': medical_history.allergies or 'None',
                    'chronic_conditions': medical_history.chronic_conditions or 'None',
                    'current_medications': medical_history.current_medications or 'None',
                    'previous_surgeries': medical_history.previous_surgeries or 'None',
                    'family_history': medical_history.family_history or 'None'
                }
            else:
                info['medical_history'] = {
                    'allergies': 'No record',
                    'chronic_conditions': 'No record',
                    'current_medications': 'No record',
                    'previous_surgeries': 'No record',
                    'family_history': 'No record'
                }
        finally:
            db.close()

        return info

    async def _generate_content_for_language(self, patient_info: Dict[str, Any], surgery_info: Dict[str, Any], language: LanguageEnum) -> Dict[str, str]:
        """Generate guideline content for a specific language using AI."""

        # Build the prompt for the specific language
        prompt = self._build_prompt_for_language(patient_info, surgery_info, language)

        try:
            if self.use_local_llm:
                # Use local LLM (Ollama)
                content = await self._generate_with_ollama_for_language(prompt, language)
            else:
                # Use OpenAI
                system_message = self._get_system_message_for_language(language)
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": system_message
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

            # Try to parse the JSON formatted response
            try:
                parsed_content = json.loads(content)
                return parsed_content
            except json.JSONDecodeError:
                # If not in JSON format, use the default template
                return self._parse_text_response(content, language)

        except Exception as e:
            logger.error(f"Error generating content with AI: {str(e)}")
            # Use the default template
            return self._get_default_template_for_language(surgery_info['anesthesia_type'], language)

    async def _generate_content(self, patient_info: Dict[str, Any], surgery_info: Dict[str, Any]) -> Dict[str, str]:
        """Generate guideline content using AI (legacy method)."""
        return await self._generate_content_for_language(patient_info, surgery_info, LanguageEnum.EN)

    def _build_prompt_for_language(self, patient_info: Dict[str, Any], surgery_info: Dict[str, Any], language: LanguageEnum) -> str:
        """Build the AI prompt for a specific language."""
        language_instructions = {
            LanguageEnum.EN: "Please generate detailed pre-anesthesia instructions based on the following patient and surgery information:",
            LanguageEnum.ZH: "請根據以下患者和手術信息生成詳細的麻醉前須知：",
            LanguageEnum.FR: "Veuillez générer des instructions détaillées de pré-anesthésie basées sur les informations suivantes sur le patient et la chirurgie :"
        }

        json_format_instructions = {
            LanguageEnum.EN: """Please generate the following content and return it in JSON format:

{
    "anesthesia_type_info": "Detailed explanation of the anesthesia type",
    "surgery_process": "Detailed description of the surgical process",
    "expected_sensations": "Various sensations the patient might experience",
    "potential_risks": "Possible risks and complications",
    "pre_surgery_instructions": "Pre-surgery preparation instructions",
    "fasting_instructions": "Specific times and precautions for fasting (NPO)",
    "medication_instructions": "Instructions for discontinuing medications",
    "common_questions": "Frequently asked questions and answers",
    "post_surgery_care": "Post-surgery care instructions"
}

Please ensure the content is professional, detailed, and easy to understand.""",
            LanguageEnum.ZH: """請生成以下內容並以JSON格式返回：

{
    "anesthesia_type_info": "麻醉類型的詳細說明",
    "surgery_process": "手術過程的詳細描述",
    "expected_sensations": "患者可能經歷的各種感受",
    "potential_risks": "可能的風險和併發症",
    "pre_surgery_instructions": "術前準備指示",
    "fasting_instructions": "禁食禁水的具體時間和注意事項",
    "medication_instructions": "停藥指示",
    "common_questions": "常見問題和答案",
    "post_surgery_care": "術後照護指示"
}

請確保內容專業、詳細且易於理解。""",
            LanguageEnum.FR: """Veuillez générer le contenu suivant et le retourner au format JSON :

{
    "anesthesia_type_info": "Explication détaillée du type d'anesthésie",
    "surgery_process": "Description détaillée du processus chirurgical",
    "expected_sensations": "Diverses sensations que le patient pourrait ressentir",
    "potential_risks": "Risques et complications possibles",
    "pre_surgery_instructions": "Instructions de préparation pré-chirurgicale",
    "fasting_instructions": "Temps spécifiques et précautions pour le jeûne (NPO)",
    "medication_instructions": "Instructions pour l'arrêt des médicaments",
    "common_questions": "Questions fréquemment posées et réponses",
    "post_surgery_care": "Instructions de soins post-chirurgicaux"
}

Veuillez vous assurer que le contenu est professionnel, détaillé et facile à comprendre."""
        }

        prompt = f"""
{language_instructions[language]}

Patient Basic Information:
- Name: {patient_info['basic_info']['name']}
- Age: {patient_info['basic_info']['age']} years old
- Gender: {patient_info['basic_info']['gender']}

Medical History:
- Allergies: {patient_info['medical_history']['allergies']}
- Chronic Conditions: {patient_info['medical_history']['chronic_conditions']}
- Current Medications: {patient_info['medical_history']['current_medications']}
- Previous Surgeries: {patient_info['medical_history']['previous_surgeries']}
- Family History: {patient_info['medical_history']['family_history']}

Surgery Information:
- Surgery Name: {surgery_info['surgery_name']}
- Anesthesia Type: {surgery_info['anesthesia_type']}
- Surgery Date: {surgery_info['surgery_date']}

{json_format_instructions[language]}
        """
        return prompt

    def _build_prompt(self, patient_info: Dict[str, Any], surgery_info: Dict[str, Any]) -> str:
        """Build the AI prompt (legacy method)."""
        return self._build_prompt_for_language(patient_info, surgery_info, LanguageEnum.EN)

    def _get_system_message_for_language(self, language: LanguageEnum) -> str:
        """Get system message for specific language."""
        system_messages = {
            LanguageEnum.EN: "You are a professional anesthesiologist. Based on the patient and surgery information, please generate detailed pre-anesthesia instructions. Please respond in English with content that is professional, easy to understand, and suitable for patients.",
            LanguageEnum.ZH: "您是一位專業的麻醉醫師。請根據患者和手術信息生成詳細的麻醉前須知。請用中文回應，內容要專業、易懂且適合患者閱讀。",
            LanguageEnum.FR: "Vous êtes un anesthésiste professionnel. Basé sur les informations du patient et de la chirurgie, veuillez générer des instructions détaillées de pré-anesthésie. Veuillez répondre en français avec un contenu professionnel, facile à comprendre et adapté aux patients."
        }
        return system_messages[language]

    def _parse_text_response(self, content: str, language: LanguageEnum = LanguageEnum.EN) -> Dict[str, str]:
        """Parse text response."""
        # Text parsing logic can be implemented here.
        # For now, using the default template.
        return self._get_default_template_for_language('general', language)

    def _get_default_template_for_language(self, anesthesia_type: str, language: LanguageEnum) -> Dict[str, str]:
        """Get the default template for specific language."""
        templates = {
            LanguageEnum.EN: {
                'general': {
                    'anesthesia_type_info': 'General anesthesia is a type of anesthesia that causes you to lose consciousness completely during surgery. The anesthesiologist will use intravenous injections and anesthetic gases to ensure you are completely unconscious during the procedure.',
                    'surgery_process': 'The surgery will be performed while you are completely unconscious. The anesthesiologist will monitor your vital signs throughout the procedure to ensure your safety.',
                    'expected_sensations': 'You will not feel any pain or discomfort. After the surgery, you will gradually regain consciousness and may feel slightly dizzy or nauseous.',
                    'potential_risks': 'Possible risks include: nausea, vomiting, sore throat, dizziness, muscle pain, etc. Serious complications are extremely rare but can include allergic reactions and breathing problems.',
                    'pre_surgery_instructions': 'Please follow the doctor\'s instructions for pre-surgery preparation, including fasting, stopping certain medications, etc.',
                    'fasting_instructions': 'Fast (no food) for 8 hours before surgery and stop drinking water 2 hours before. This is to prevent the risk of vomiting and aspiration pneumonia during anesthesia.',
                    'medication_instructions': 'Please inform your doctor of all medications you are currently taking. Some medications (such as blood thinners) may need to be stopped in advance.',
                    'common_questions': 'Q: Are there side effects to anesthesia?\nA: Most patients experience only minor side effects, such as nausea and dizziness, which usually disappear within 24 hours.',
                    'post_surgery_care': 'After surgery, please follow the doctor\'s instructions for care, including wound care, medication, and activity restrictions. If you experience any abnormalities, seek medical attention immediately.'
                },
                'local': {
                    'anesthesia_type_info': 'Local anesthesia numbs only the surgical area, allowing you to remain awake during the procedure.',
                    'surgery_process': 'You will remain awake during the surgery, but you will not feel pain in the surgical area.',
                    'expected_sensations': 'The surgical area will feel numb, but not painful. You may feel touch or pressure, but no pain.',
                    'potential_risks': 'Possible risks include: pain at the injection site, bruising, infection, etc. Serious complications are extremely rare.',
                    'pre_surgery_instructions': 'Please follow the doctor\'s instructions for pre-surgery preparation.',
                    'fasting_instructions': 'Fasting is usually not required, but please follow your doctor\'s instructions.',
                    'medication_instructions': 'Please inform your doctor of all medications you are currently taking.',
                    'common_questions': 'Q: Is local anesthesia painful?\nA: There will be a slight sting during the injection, but it will quickly become numb.',
                    'post_surgery_care': 'After surgery, please follow the doctor\'s instructions for care. The anesthetic effect usually lasts for several hours.'
                }
            },
            LanguageEnum.ZH: {
                'general': {
                    'anesthesia_type_info': '全身麻醉是一種在手術過程中讓您完全失去意識的麻醉方式。麻醉醫師會使用靜脈注射和麻醉氣體來確保您在手術過程中完全無意識。',
                    'surgery_process': '手術將在您完全無意識的狀態下進行。麻醉醫師會在手術過程中監控您的生命體徵，確保您的安全。',
                    'expected_sensations': '您不會感到任何疼痛或不適。手術後，您會逐漸恢復意識，可能會感到輕微的頭暈或噁心。',
                    'potential_risks': '可能的風險包括：噁心、嘔吐、喉嚨痛、頭暈、肌肉疼痛等。嚴重併發症極為罕見，但可能包括過敏反應和呼吸問題。',
                    'pre_surgery_instructions': '請遵循醫師的術前準備指示，包括禁食、停用某些藥物等。',
                    'fasting_instructions': '手術前8小時禁食，手術前2小時停止飲水。這是為了防止麻醉期間嘔吐和吸入性肺炎的風險。',
                    'medication_instructions': '請告知醫師您目前正在服用的所有藥物。某些藥物（如抗凝血劑）可能需要提前停用。',
                    'common_questions': '問：麻醉有副作用嗎？\n答：大多數患者只會出現輕微的副作用，如噁心和頭暈，通常在24小時內消失。',
                    'post_surgery_care': '手術後，請遵循醫師的照護指示，包括傷口護理、藥物使用和活動限制。如有任何異常，請立即就醫。'
                },
                'local': {
                    'anesthesia_type_info': '局部麻醉只會麻醉手術區域，讓您在手術過程中保持清醒。',
                    'surgery_process': '您在手術過程中會保持清醒，但手術區域不會感到疼痛。',
                    'expected_sensations': '手術區域會感到麻木，但不會疼痛。您可能會感到觸摸或壓力，但不會感到疼痛。',
                    'potential_risks': '可能的風險包括：注射部位疼痛、瘀血、感染等。嚴重併發症極為罕見。',
                    'pre_surgery_instructions': '請遵循醫師的術前準備指示。',
                    'fasting_instructions': '通常不需要禁食，但請遵循醫師的指示。',
                    'medication_instructions': '請告知醫師您目前正在服用的所有藥物。',
                    'common_questions': '問：局部麻醉會痛嗎？\n答：注射時會有輕微刺痛，但很快就會麻木。',
                    'post_surgery_care': '手術後，請遵循醫師的照護指示。麻醉效果通常持續數小時。'
                }
            },
            LanguageEnum.FR: {
                'general': {
                    'anesthesia_type_info': 'L\'anesthésie générale est un type d\'anesthésie qui vous fait perdre complètement conscience pendant la chirurgie. L\'anesthésiste utilisera des injections intraveineuses et des gaz anesthésiques pour s\'assurer que vous êtes complètement inconscient pendant la procédure.',
                    'surgery_process': 'La chirurgie sera effectuée pendant que vous êtes complètement inconscient. L\'anesthésiste surveillera vos signes vitaux tout au long de la procédure pour assurer votre sécurité.',
                    'expected_sensations': 'Vous ne ressentirez aucune douleur ou inconfort. Après la chirurgie, vous reprendrez progressivement conscience et pourriez ressentir des étourdissements légers ou des nausées.',
                    'potential_risks': 'Les risques possibles incluent : nausées, vomissements, maux de gorge, étourdissements, douleurs musculaires, etc. Les complications graves sont extrêmement rares mais peuvent inclure des réactions allergiques et des problèmes respiratoires.',
                    'pre_surgery_instructions': 'Veuillez suivre les instructions du médecin pour la préparation pré-chirurgicale, y compris le jeûne, l\'arrêt de certains médicaments, etc.',
                    'fasting_instructions': 'Jeûnez (pas de nourriture) pendant 8 heures avant la chirurgie et arrêtez de boire de l\'eau 2 heures avant. Ceci est pour prévenir le risque de vomissement et de pneumonie d\'aspiration pendant l\'anesthésie.',
                    'medication_instructions': 'Veuillez informer votre médecin de tous les médicaments que vous prenez actuellement. Certains médicaments (comme les anticoagulants) peuvent devoir être arrêtés à l\'avance.',
                    'common_questions': 'Q: Y a-t-il des effets secondaires à l\'anesthésie ?\nR: La plupart des patients ne ressentent que des effets secondaires mineurs, comme des nausées et des étourdissements, qui disparaissent généralement dans les 24 heures.',
                    'post_surgery_care': 'Après la chirurgie, veuillez suivre les instructions du médecin pour les soins, y compris les soins de la plaie, les médicaments et les restrictions d\'activité. Si vous ressentez des anomalies, consultez immédiatement un médecin.'
                },
                'local': {
                    'anesthesia_type_info': 'L\'anesthésie locale engourdit seulement la zone chirurgicale, vous permettant de rester éveillé pendant la procédure.',
                    'surgery_process': 'Vous resterez éveillé pendant la chirurgie, mais vous ne ressentirez pas de douleur dans la zone chirurgicale.',
                    'expected_sensations': 'La zone chirurgicale sera engourdie, mais pas douloureuse. Vous pourriez ressentir du toucher ou de la pression, mais pas de douleur.',
                    'potential_risks': 'Les risques possibles incluent : douleur au site d\'injection, ecchymoses, infection, etc. Les complications graves sont extrêmement rares.',
                    'pre_surgery_instructions': 'Veuillez suivre les instructions du médecin pour la préparation pré-chirurgicale.',
                    'fasting_instructions': 'Le jeûne n\'est généralement pas requis, mais veuillez suivre les instructions de votre médecin.',
                    'medication_instructions': 'Veuillez informer votre médecin de tous les médicaments que vous prenez actuellement.',
                    'common_questions': 'Q: L\'anesthésie locale est-elle douloureuse ?\nR: Il y aura une légère piqûre pendant l\'injection, mais elle deviendra rapidement engourdie.',
                    'post_surgery_care': 'Après la chirurgie, veuillez suivre les instructions du médecin pour les soins. L\'effet anesthésique dure généralement plusieurs heures.'
                }
            }
        }
        return templates[language].get(anesthesia_type, templates[language]['general'])

    def _parse_text_response(self, content: str) -> Dict[str, str]:
        """Parse text response (legacy method)."""
        # Text parsing logic can be implemented here.
        # For now, using the default template.
        return self._get_default_template('general')

    def _get_default_template(self, anesthesia_type: str) -> Dict[str, str]:
        """Get the default template."""
        templates = {
            'general': {
                'anesthesia_type_info': 'General anesthesia is a type of anesthesia that causes you to lose consciousness completely during surgery. The anesthesiologist will use intravenous injections and anesthetic gases to ensure you are completely unconscious during the procedure.',
                'surgery_process': 'The surgery will be performed while you are completely unconscious. The anesthesiologist will monitor your vital signs throughout the procedure to ensure your safety.',
                'expected_sensations': 'You will not feel any pain or discomfort. After the surgery, you will gradually regain consciousness and may feel slightly dizzy or nauseous.',
                'potential_risks': 'Possible risks include: nausea, vomiting, sore throat, dizziness, muscle pain, etc. Serious complications are extremely rare but can include allergic reactions and breathing problems.',
                'pre_surgery_instructions': 'Please follow the doctor\'s instructions for pre-surgery preparation, including fasting, stopping certain medications, etc.',
                'fasting_instructions': 'Fast (no food) for 8 hours before surgery and stop drinking water 2 hours before. This is to prevent the risk of vomiting and aspiration pneumonia during anesthesia.',
                'medication_instructions': 'Please inform your doctor of all medications you are currently taking. Some medications (such as blood thinners) may need to be stopped in advance.',
                'common_questions': 'Q: Are there side effects to anesthesia?\nA: Most patients experience only minor side effects, such as nausea and dizziness, which usually disappear within 24 hours.',
                'post_surgery_care': 'After surgery, please follow the doctor\'s instructions for care, including wound care, medication, and activity restrictions. If you experience any abnormalities, seek medical attention immediately.'
            },
            'local': {
                'anesthesia_type_info': 'Local anesthesia numbs only the surgical area, allowing you to remain awake during the procedure.',
                'surgery_process': 'You will remain awake during the surgery, but you will not feel pain in the surgical area.',
                'expected_sensations': 'The surgical area will feel numb, but not painful. You may feel touch or pressure, but no pain.',
                'potential_risks': 'Possible risks include: pain at the injection site, bruising, infection, etc. Serious complications are extremely rare.',
                'pre_surgery_instructions': 'Please follow the doctor\'s instructions for pre-surgery preparation.',
                'fasting_instructions': 'Fasting is usually not required, but please follow your doctor\'s instructions.',
                'medication_instructions': 'Please inform your doctor of all medications you are currently taking.',
                'common_questions': 'Q: Is local anesthesia painful?\nA: There will be a slight sting during the injection, but it will quickly become numb.',
                'post_surgery_care': 'After surgery, please follow the doctor\'s instructions for care. The anesthetic effect usually lasts for several hours.'
            }
        }
        return templates.get(anesthesia_type, templates['general'])

    def _calculate_age(self, date_of_birth: date) -> int:
        """Calculate age."""
        today = date.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    def _get_gender_display(self, gender: str) -> str:
        """Get gender display text."""
        gender_map = {
            'M': 'Male',
            'F': 'Female',
            'O': 'Other'
        }
        return gender_map.get(gender, 'Unknown')

    async def _generate_with_ollama_for_language(self, prompt: str, language: LanguageEnum) -> str:
        """Generate content using Ollama for specific language."""
        try:
            system_message = self._get_system_message_for_language(language)

            # Build Ollama API request
            payload = {
                "model": self.ollama_model,
                "prompt": f"{system_message}\n\n{prompt}",
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
                logger.error(f"Ollama API error: {response.status_code}")
                raise Exception(f"Ollama API error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Ollama service. Please ensure Ollama is running.")
            raise Exception("Could not connect to Ollama service")
        except Exception as e:
            logger.error(f"Error generating content with Ollama: {str(e)}")
            raise

    async def _generate_with_ollama(self, prompt: str) -> str:
        """Generate content using Ollama (legacy method)."""
        return await self._generate_with_ollama_for_language(prompt, LanguageEnum.EN)
