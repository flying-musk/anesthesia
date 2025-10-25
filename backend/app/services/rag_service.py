"""
RAG 问答服务模块
使用 LangChain + Ollama 实现麻醉知识问答
"""

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.llms import Ollama
except ImportError:
    print("Warning: langchain_community not available")
    OllamaEmbeddings = None
    Chroma = None
    Ollama = None

import os
from pathlib import Path


class AnesthesiaRAG:
    def __init__(self):
        self.llm = None
        self.embedding = None
        self.vectorstore_en = None
        self.vectorstore_zh = None

        try:
            if Ollama is not None:
                self.llm = Ollama(model="llama3:8b", temperature=0.3)
                self.embedding = OllamaEmbeddings(model="llama3:8b")
                self.initialize_vectorstores()
            else:
                print("⚠️  Ollama not available")
        except Exception as e:
            print(f"⚠️  Ollama 初始化失败: {e}")

    def initialize_vectorstores(self):
        """初始化向量数据库"""
        try:
            from app.utils.knowledge_base_en import ANESTHESIA_KNOWLEDGE_EN

            # 创建数据目录
            base_dir = Path(__file__).parent.parent.parent.parent
            persist_dir_en = base_dir / "data" / "chroma_db_en"
            persist_dir_en.mkdir(parents=True, exist_ok=True)

            persist_dir_en_str = str(persist_dir_en)

            # 检查是否已存在向量数据库
            if os.path.exists(persist_dir_en_str) and os.listdir(persist_dir_en_str):
                try:
                    self.vectorstore_en = Chroma(
                        persist_directory=persist_dir_en_str,
                        embedding_function=self.embedding
                    )
                    print("✅ 已加载现有向量数据库")
                except:
                    print("⚠️  加载现有数据库失败，将创建新的")
                    self.vectorstore_en = None

            if self.vectorstore_en is None:
                # 创建新的向量数据库
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=50,
                    separators=["\n\n", "\n", ". ", " "]
                )
                texts_en = text_splitter.create_documents([ANESTHESIA_KNOWLEDGE_EN])
                self.vectorstore_en = Chroma.from_documents(
                    documents=texts_en,
                    embedding=self.embedding,
                    persist_directory=persist_dir_en_str
                )
                self.vectorstore_en.persist()
                print("✅ 已创建新的向量数据库")

            # 暂时只使用英文知识库
            self.vectorstore_zh = self.vectorstore_en

            print("✅ RAG 系统初始化成功")
        except Exception as e:
            print(f"⚠️  RAG 向量数据库初始化失败: {e}")

    def answer_question(self, question: str, language: str = "en") -> dict:
        """回答问题 - 支持多语言"""

        # 如果 LLM 未初始化，返回错误信息
        if not self.llm or not self.vectorstore_en:
            return {
                "answer": "RAG system is not available. Please make sure Ollama is running with llama3:8b model.",
                "needs_doctor": True,
                "category": "error",
                "confidence": "low",
                "source_documents": 0
            }

        try:
            # 检索相关文档
            vectorstore = self.vectorstore_en if language == "en" else self.vectorstore_zh
            docs = vectorstore.similarity_search(question, k=3)

            # 构建上下文
            context = "\n\n".join([doc.page_content for doc in docs])

            # 构建提示词
            if language == "en":
                prompt = f"""You are a professional anesthesiologist. Answer the following question in English based on the provided context.

Requirements:
1. Use simple, clear language that patients can understand
2. Be warm, friendly, and reassuring
3. If the question involves personal medical conditions, suggest consulting with their doctor
4. Base your answer on the provided context
5. Keep answers concise (2-3 paragraphs maximum)

Context:
{context}

Question: {question}

Answer:"""
            elif language == "es":
                prompt = f"""You are a professional anesthesiologist. Answer the following question in Spanish based on the provided context.

Context:
{context}

Question: {question}

Answer:"""
            elif language == "fr":
                prompt = f"""Vous êtes un anesthésiste professionnel. Répondez à la question suivante en français.

Context:
{context}

Question: {question}

Réponse:"""
            else:  # zh-TW
                prompt = f"""你是一位專業的麻醉醫師。請用繁體中文回答以下問題。

上下文：
{context}

問題：{question}

回答："""

            # 获取答案
            answer = self.llm.invoke(prompt)

            # 判断是否需要医师介入
            needs_doctor = self._check_needs_doctor(question, language)

            # 分类问题
            category = self._categorize_question(question, language)

            # 计算信心度
            confidence = "high" if len(docs) >= 2 else "medium"

            return {
                "answer": answer,
                "needs_doctor": needs_doctor,
                "category": category,
                "confidence": confidence,
                "source_documents": len(docs)
            }
        except Exception as e:
            return {
                "answer": f"Error processing question: {str(e)}",
                "needs_doctor": True,
                "category": "error",
                "confidence": "low",
                "source_documents": 0
            }

    def _check_needs_doctor(self, question: str, language: str) -> bool:
        """检查是否需要医师介入"""
        try:
            from app.utils.knowledge_base_en import DOCTOR_INTERVENTION_KEYWORDS_EN
            keywords = DOCTOR_INTERVENTION_KEYWORDS_EN
        except:
            keywords = [
                "allergic", "allergy", "heart", "pregnant", "medication",
                "medical history", "worried", "concerned"
            ]

        question_lower = question.lower()
        return any(keyword.lower() in question_lower for keyword in keywords)

    def _categorize_question(self, question: str, language: str) -> str:
        """分类问题"""
        try:
            from app.utils.knowledge_base_en import FAQ_CATEGORIES_EN
            categories = FAQ_CATEGORIES_EN
        except:
            categories = {
                "safety": ["safe", "risk", "danger"],
                "pain": ["pain", "hurt"],
                "side_effects": ["side effect", "nausea"],
                "process": ["process", "how", "what happens"],
            }

        question_lower = question.lower()
        for category, keywords in categories.items():
            if any(keyword.lower() in question_lower for keyword in keywords):
                return category
        return "general"


# 全局实例
rag_system = None

def get_rag_system():
    """获取 RAG 系统实例"""
    global rag_system
    if rag_system is None:
        rag_system = AnesthesiaRAG()
    return rag_system
