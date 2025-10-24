"""
Anesthesia Guideline Generation Service
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
    """Service for generating anesthesia guidelines."""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.ollama_url = settings.OLLAMA_URL
        self.ollama_model = settings.OLLAMA_MODEL
        self.use_local_llm = settings.USE_LOCAL_LLM
    
    async def generate_guideline(self, db, request: GenerateGuidelineRequest) -> AnesthesiaGuideline:
        """Generate anesthesia guideline."""
        try:
            # Get patient information
            patient = db.query(Patient).filter(Patient.id == request.patient_id).first()
            if not patient:
                raise ValueError("Patient not found")
            
            # Prepare patient medical information
            patient_info = self._prepare_patient_info(patient)
            
            # Generate guideline content
            guideline_content = await self._generate_content(patient_info, request.dict())
            
            # Create anesthesia guideline record
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
    
    async def _generate_content(self, patient_info: Dict[str, Any], surgery_info: Dict[str, Any]) -> Dict[str, str]:
        """Generate guideline content using AI."""
        
        # Build the prompt
        prompt = self._build_prompt(patient_info, surgery_info)
        
        try:
            if self.use_local_llm:
                # Use local LLM (Ollama)
                content = await self._generate_with_ollama(prompt)
            else:
                # Use OpenAI
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional anesthesiologist. Based on the patient and surgery information, please generate detailed pre-anesthesia instructions. Please respond in English with content that is professional, easy to understand, and suitable for patients."
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
                return self._parse_text_response(content)
                
        except Exception as e:
            logger.error(f"Error generating content with AI: {str(e)}")
            # Use the default template
            return self._get_default_template(surgery_info['anesthesia_type'])
    
    def _build_prompt(self, patient_info: Dict[str, Any], surgery_info: Dict[str, Any]) -> str:
        """Build the AI prompt."""
        prompt = f"""
Please generate detailed pre-anesthesia instructions based on the following patient and surgery information:

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

Please generate the following content and return it in JSON format:

{{
    "anesthesia_type_info": "Detailed explanation of the anesthesia type",
    "surgery_process": "Detailed description of the surgical process",
    "expected_sensations": "Various sensations the patient might experience",
    "potential_risks": "Possible risks and complications",
    "pre_surgery_instructions": "Pre-surgery preparation instructions",
    "fasting_instructions": "Specific times and precautions for fasting (NPO)",
    "medication_instructions": "Instructions for discontinuing medications",
    "common_questions": "Frequently asked questions and answers",
    "post_surgery_care": "Post-surgery care instructions"
}}

Please ensure the content is professional, detailed, and easy to understand.
        """
        return prompt
    
    def _parse_text_response(self, content: str) -> Dict[str, str]:
        """Parse text response."""
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
    
    async def _generate_with_ollama(self, prompt: str) -> str:
        """Generate content using Ollama."""
        try:
            # Build Ollama API request
            payload = {
                "model": self.ollama_model,
                "prompt": f"You are a professional anesthesiologist. Based on the patient and surgery information, please generate detailed pre-anesthesia instructions. Please respond in English with content that is professional, easy to understand, and suitable for patients.\n\n{prompt}",
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
