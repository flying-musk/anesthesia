"""
问答 API 端点
基于 RAG 的麻醉知识问答
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.rag_service import get_rag_system

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str
    language: str = "en"  # en, zh-TW, es, fr


class QuestionResponse(BaseModel):
    answer: str
    needs_doctor: bool
    category: str
    confidence: str
    suggested_action: str


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """患者提问接口 - 支持多语言"""
    try:
        rag = get_rag_system()
        result = rag.answer_question(
            question=request.question,
            language=request.language
        )

        # 根据语言返回建议
        lang_suggestions = {
            "en": {
                "doctor": "Please discuss this with your anesthesiologist",
                "ai": "This question has been answered by AI"
            },
            "es": {
                "doctor": "Por favor, consulte con su anestesiólogo",
                "ai": "Esta pregunta ha sido respondida por IA"
            },
            "fr": {
                "doctor": "Veuillez en discuter avec votre anesthésiste",
                "ai": "Cette question a été répondue par l'IA"
            },
            "zh-TW": {
                "doctor": "請與麻醉醫師討論此問題",
                "ai": "此問題已由AI回答"
            }
        }

        suggestions = lang_suggestions.get(request.language, lang_suggestions["en"])
        suggested_action = suggestions["doctor"] if result["needs_doctor"] else suggestions["ai"]

        return QuestionResponse(
            answer=result["answer"],
            needs_doctor=result["needs_doctor"],
            category=result["category"],
            confidence=result["confidence"],
            suggested_action=suggested_action
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/common-questions")
async def get_common_questions(language: str = "en"):
    """获取常见问题列表"""

    questions = {
        "en": [
            "Is general anesthesia safe?",
            "Will I wake up during surgery?",
            "What are the side effects of anesthesia?",
            "How long should I fast before surgery?",
            "How long does it take to wake up?",
            "Will anesthesia affect my memory?",
            "Can I have anesthesia if I have allergies?",
            "What's the difference between spinal and epidural?",
            "Will I feel pain during surgery?",
            "What happens in the recovery room?"
        ],
        "es": [
            "¿Es segura la anestesia general?",
            "¿Me despertaré durante la cirugía?",
            "¿Cuáles son los efectos secundarios?",
            "¿Cuánto tiempo debo ayunar?",
            "¿Cuánto tiempo tarda en despertar?",
            "¿Qué es la anestesia espinal?",
            "¿Puedo tener anestesia si tengo alergias?",
            "¿Sentiré dolor durante la cirugía?"
        ],
        "fr": [
            "L'anesthésie générale est-elle sûre?",
            "Vais-je me réveiller pendant la chirurgie?",
            "Quels sont les effets secondaires?",
            "Combien de temps dois-je jeûner?",
            "Combien de temps faut-il pour se réveiller?",
            "L'anesthésie affectera-t-elle ma mémoire?"
        ],
        "zh-TW": [
            "全身麻醉安全嗎？",
            "我會在手術中醒來嗎？",
            "麻醉後會有什麼副作用？",
            "麻醉前需要禁食多久？",
            "醒來需要多長時間？",
            "麻醉會影響記憶嗎？",
            "脊髓麻醉和硬膜外麻醉有什麼區別？",
            "什麼情況下不能使用全身麻醉？"
        ]
    }

    return {"questions": questions.get(language, questions["en"])}


@router.get("/health")
async def health_check():
    """健康检查"""
    try:
        rag = get_rag_system()
        return {
            "status": "healthy",
            "vectorstore_en": rag.vectorstore_en is not None,
            "llm_available": rag.llm is not None
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
