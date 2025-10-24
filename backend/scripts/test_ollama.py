#!/usr/bin/env python
"""
測試Ollama連接腳本
"""

import requests
import json

def test_ollama_connection():
    """測試Ollama連接"""
    print("🔍 測試Ollama連接...")
    
    try:
        # 測試連接
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama服務正在運行")
            print(f"📋 可用模型: {len(models.get('models', []))}個")
            
            for model in models.get('models', []):
                print(f"  - {model['name']}")
            
            return True
        else:
            print(f"❌ Ollama服務回應錯誤: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到Ollama服務")
        print("💡 請確保Ollama正在運行: ollama serve")
        return False
    except Exception as e:
        print(f"❌ 測試失敗: {str(e)}")
        return False

def test_model_generation():
    """測試模型生成"""
    print("\n🤖 測試模型生成...")
    
    try:
        payload = {
            "model": "qwen2.5:7b",
            "prompt": "請用繁體中文簡短介紹什麼是麻醉。",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("response", "")
            print("✅ 模型生成成功")
            print(f"📝 回應內容: {content[:200]}...")
            return True
        else:
            print(f"❌ 模型生成失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {str(e)}")
        return False

def main():
    """主函數"""
    print("🚀 Ollama測試開始...")
    print("=" * 50)
    
    # 測試連接
    connection_ok = test_ollama_connection()
    
    if connection_ok:
        # 測試生成
        generation_ok = test_model_generation()
        
        if generation_ok:
            print("\n🎉 Ollama測試完全成功！")
            print("✅ 你現在可以使用本地LLM來生成麻醉須知了！")
        else:
            print("\n⚠️ Ollama連接正常，但模型生成有問題")
            print("💡 請檢查模型是否已下載: ollama pull qwen2.5:7b")
    else:
        print("\n❌ Ollama測試失敗")
        print("💡 請按照以下步驟設定Ollama:")
        print("1. 下載並安裝Ollama: https://ollama.ai/download")
        print("2. 啟動服務: ollama serve")
        print("3. 下載模型: ollama pull qwen2.5:7b")

if __name__ == "__main__":
    main()
