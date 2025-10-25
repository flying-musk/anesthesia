"""
Ollama 服務
"""

import httpx
import asyncio
from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class OllamaService:
    """Ollama 服務類"""
    
    def __init__(self):
        self.ollama_url = settings.OLLAMA_URL
        self.ollama_model = settings.OLLAMA_MODEL
    
    async def generate_text(self, prompt: str) -> str:
        """使用 Ollama 生成文本"""
        try:
            # Build Ollama API request
            request_data = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json=request_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "").strip()
                else:
                    logger.error(f"Ollama API error: {response.status_code}")
                    raise Exception(f"Ollama API error: {response.status_code}")
                        
        except httpx.ConnectError:
            logger.error("Could not connect to Ollama service. Please ensure Ollama is running.")
            raise Exception("Could not connect to Ollama service")
        except Exception as e:
            logger.error(f"Error generating content with Ollama: {str(e)}")
            raise e
