"""
翻译服务模块
使用 Ollama 进行字幕翻译，集成医学术语词典
"""

from langchain_community.llms import Ollama
from sqlalchemy.orm import Session
from app.models.video import Terminology
import re


class TranslationService:
    """翻译服务"""

    def __init__(self, model_name: str = "llama3:8b"):
        try:
            self.llm = Ollama(model=model_name, temperature=0.3)
        except Exception as e:
            print(f"⚠️  Ollama 初始化失败: {e}")
            self.llm = None

        self.terminology_cache = {}

    def load_terminology(self, db: Session):
        """加载医学术语词典"""
        try:
            terms = db.query(Terminology).all()
            for term in terms:
                self.terminology_cache[term.term_en.lower()] = {
                    'en': term.term_en,
                    'zh': term.term_zh,
                    'es': term.term_es,
                    'ja': term.term_ja,
                    'fr': term.term_fr,
                }
            print(f"✅ 已加载 {len(self.terminology_cache)} 条医学术语")
        except Exception as e:
            print(f"⚠️  加载术语词典失败: {e}")

    def translate(
        self,
        text: str,
        target_language: str,
        source_language: str = 'en',
        use_terminology: bool = True
    ) -> str:
        """
        翻译文本

        Args:
            text: 原文
            target_language: 目标语言代码 ('zh-TW', 'es', 'ja', 'fr' 等)
            source_language: 源语言代码
            use_terminology: 是否使用术语词典

        Returns:
            翻译后的文本
        """
        if not self.llm:
            return f"[Translation service not available]"

        # 提取术语并替换为占位符
        terms_found = []
        text_with_placeholders = text
        lang_code = target_language.split('-')[0]  # zh-TW -> zh

        # 检查该语言是否有术语表
        has_terminology = False
        if use_terminology and self.terminology_cache:
            for term_en, translations in self.terminology_cache.items():
                if translations.get(lang_code):
                    has_terminology = True
                    break

        if use_terminology and has_terminology:
            for term_en, translations in self.terminology_cache.items():
                pattern = re.compile(re.escape(term_en), re.IGNORECASE)
                if pattern.search(text.lower()):
                    placeholder = f"[TERM_{len(terms_found)}]"
                    terms_found.append({
                        'en': term_en,
                        'translation': translations.get(lang_code)
                    })
                    text_with_placeholders = pattern.sub(placeholder, text_with_placeholders)

        # 构建翻译提示词
        lang_map = {
            'zh-TW': 'Traditional Chinese (繁體中文)',
            'zh': 'Simplified Chinese (简体中文)',
            'es': 'Spanish (Español)',
            'ja': 'Japanese (日本語)',
            'fr': 'French (Français)',
        }

        target_lang_name = lang_map.get(target_language, target_language)
        prompt = self._build_translation_prompt(
            text_with_placeholders,
            target_lang_name,
            terms_found
        )

        # 调用LLM翻译
        try:
            translated = self.llm.invoke(prompt)
            translated = translated.strip()

            # 清除 AI 可能加入的注释和多余文本
            translated = re.sub(r'\(Note:.*?\)', '', translated, flags=re.IGNORECASE | re.DOTALL)
            translated = re.sub(r'\n\n.*?Note:.*', '', translated, flags=re.IGNORECASE | re.DOTALL)
            translated = re.sub(r'^Output:\s*', '', translated, flags=re.IGNORECASE)
            translated = re.sub(r'\n+Output:\s*', '\n', translated, flags=re.IGNORECASE)
            translated = translated.strip()

            # 替换回术语
            for idx, term_info in enumerate(terms_found):
                placeholder = f"[TERM_{idx}]"
                if term_info['translation']:
                    translated = translated.replace(placeholder, term_info['translation'])
                else:
                    translated = translated.replace(placeholder, term_info['en'])

            return translated

        except Exception as e:
            print(f"❌ 翻译失败: {e}")
            return f"[Translation Error: {str(e)}]"

    def _build_translation_prompt(
        self,
        text: str,
        target_language: str,
        terms: list
    ) -> str:
        """构建翻译提示词"""
        terms_info = ""
        if terms:
            terms_list = "\n".join([
                f"  - [TERM_{idx}]: {term['en']}"
                for idx, term in enumerate(terms)
            ])
            terms_info = f"""
Important medical terms (keep as placeholders):
{terms_list}
"""

        prompt = f"""You are a professional medical translator specializing in anesthesia content.

Task: Translate the following English text to {target_language}.

Requirements:
1. Translate to {target_language} language ONLY
2. Use clear, simple language suitable for patients
3. Maintain a warm and reassuring tone
4. Keep medical terminology accurate
5. Do NOT translate the [TERM_X] placeholders - keep them exactly as they are
6. Output ONLY the translated text in {target_language}
7. Do NOT include any notes, explanations, or comments

{terms_info}
English text:
{text}

{target_language} translation:"""

        return prompt


# 语言配置
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'zh-TW': '繁體中文',
    'zh-CN': '简体中文',
    'es': 'Español',
    'ja': '日本語',
    'fr': 'Français',
}


def get_language_name(lang_code: str) -> str:
    """获取语言名称"""
    return SUPPORTED_LANGUAGES.get(lang_code, lang_code)
