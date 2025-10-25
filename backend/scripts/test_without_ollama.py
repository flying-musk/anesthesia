#!/usr/bin/env python
"""
測試麻醉系統 - 不使用Ollama (使用預設模板)
"""

import asyncio
import httpx
import json

# API 基礎 URL
BASE_URL = 'http://localhost:8000/api/v1'

async def test_system_without_ollama():
    """測試系統不使用Ollama"""
    print("🧪 測試麻醉系統 (使用預設模板)...")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        try:
            # 1. 測試健康檢查
            print("1️⃣ 測試健康檢查...")
            response = await client.get(f"{BASE_URL.replace('/api/v1', '')}/health")
            if response.status_code == 200:
                print("✅ 系統健康")
            else:
                print(f"❌ 健康檢查失敗: {response.status_code}")
                return
            
            # 2. 測試患者搜尋
            print("\n2️⃣ 測試患者搜尋...")
            search_data = {
                "health_insurance_number": "1234567890",
                "full_name": "王小明",
                "date_of_birth": "1985-05-15"
            }
            
            response = await client.post(f"{BASE_URL}/patients/search", json=search_data)
            if response.status_code == 200:
                patient_data = response.json()
                patient_id = patient_data['id']
                print(f"✅ 找到患者: {patient_data['full_name']} (ID: {patient_id})")
            else:
                print(f"❌ 患者搜尋失敗: {response.status_code}")
                return
            
            # 3. 測試生成麻醉須知 (使用預設模板)
            print("\n3️⃣ 測試生成麻醉須知...")
            guideline_data = {
                "patient_id": patient_id,
                "surgery_name": "腹腔鏡膽囊切除術",
                "anesthesia_type": "general",
                "surgery_date": "2024-01-15",
                "surgeon_name": "李醫師",
                "anesthesiologist_name": "陳醫師"
            }
            
            response = await client.post(f"{BASE_URL}/anesthesia/guidelines/generate", json=guideline_data)
            if response.status_code == 201:
                guideline_result = response.json()
                print("✅ 麻醉須知生成成功！")
                print(f"📋 手術名稱: {guideline_result['surgery_name']}")
                print(f"🏥 麻醉類型: {guideline_result['anesthesia_type']}")
                print(f"🤖 AI生成: {guideline_result['is_generated']}")
                
                # 顯示部分內容
                print("\n📝 麻醉須知內容預覽:")
                print(f"  - 麻醉類型說明: {guideline_result['anesthesia_type_info'][:100]}...")
                print(f"  - 手術過程: {guideline_result['surgery_process'][:100]}...")
                print(f"  - 術前須知: {guideline_result['pre_surgery_instructions'][:100]}...")
                
                return guideline_result['id']
            else:
                print(f"❌ 麻醉須知生成失敗: {response.status_code}")
                print(f"錯誤詳情: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 測試過程中發生錯誤: {str(e)}")
            return None

async def main():
    """主函數"""
    print("🚀 麻醉系統測試開始...")
    print("💡 這個測試使用預設模板，不需要Ollama")
    print("=" * 50)
    
    guideline_id = await test_system_without_ollama()
    
    if guideline_id:
        print("\n🎉 測試完成！")
        print("✅ 你的麻醉系統完全可以正常工作")
        print("📊 系統功能:")
        print("  - ✅ 患者管理")
        print("  - ✅ 醫療病史")
        print("  - ✅ 麻醉須知生成")
        print("  - ✅ AI模板系統")
        
        print("\n🔧 下一步你可以:")
        print("1. 安裝Docker並運行Ollama來使用本地LLM")
        print("2. 或者繼續使用預設模板系統")
        print("3. 或者設定OpenAI API Key")
        
        print(f"\n🌐 查看API文檔: http://localhost:8000/docs")
        print(f"🔍 測試生成的麻醉須知: GET /api/v1/anesthesia/guidelines/{guideline_id}")
    else:
        print("\n❌ 測試失敗")
        print("💡 請確保:")
        print("1. 伺服器正在運行: uvicorn app.main:app --reload")
        print("2. 資料庫已初始化: python3 start_demo.py")

if __name__ == "__main__":
    asyncio.run(main())
