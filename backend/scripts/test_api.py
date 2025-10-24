#!/usr/bin/env python
"""
API 測試腳本 - FastAPI 版本
用於測試麻醉須知生成系統的 API 端點
"""

import asyncio
import httpx
import json
from datetime import date

# API 基礎 URL
BASE_URL = 'http://localhost:8000/api/v1'


async def test_patient_search():
    """測試患者搜尋"""
    print("測試患者搜尋...")
    
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/patients/search"
        data = {
            "health_insurance_number": "1234567890",
            "full_name": "王小明",
            "date_of_birth": "1985-05-15"
        }
        
        response = await client.post(url, json=data)
        print(f"狀態碼: {response.status_code}")
        if response.status_code == 200:
            patient_data = response.json()
            print(f"找到患者: {patient_data['full_name']}")
            return patient_data['id']
        else:
            print(f"錯誤: {response.text}")
            return None


async def test_generate_guideline(patient_id):
    """測試生成麻醉須知"""
    print("測試生成麻醉須知...")
    
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/anesthesia/guidelines/generate"
        data = {
            "patient_id": patient_id,
            "surgery_name": "腹腔鏡膽囊切除術",
            "anesthesia_type": "general",
            "surgery_date": "2024-01-15",
            "surgeon_name": "李醫師",
            "anesthesiologist_name": "陳醫師"
        }
        
        response = await client.post(url, json=data)
        print(f"狀態碼: {response.status_code}")
        if response.status_code == 201:
            guideline_data = response.json()
            print("麻醉須知生成成功！")
            print(f"手術名稱: {guideline_data['surgery_name']}")
            print(f"麻醉類型: {guideline_data['anesthesia_type']}")
            print(f"是否已生成: {guideline_data['is_generated']}")
            return guideline_data['id']
        else:
            print(f"錯誤: {response.text}")
            return None


async def test_get_guideline(guideline_id):
    """測試獲取麻醉須知"""
    print("測試獲取麻醉須知...")
    
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/anesthesia/guidelines/{guideline_id}"
        response = await client.get(url)
        print(f"狀態碼: {response.status_code}")
        if response.status_code == 200:
            guideline_data = response.json()
            print("麻醉須知內容:")
            print(f"- 麻醉類型說明: {guideline_data['anesthesia_type_info'][:100]}...")
            print(f"- 手術過程: {guideline_data['surgery_process'][:100]}...")
            print(f"- 預期感受: {guideline_data['expected_sensations'][:100]}...")
            print(f"- 可能風險: {guideline_data['potential_risks'][:100]}...")
            print(f"- 術前須知: {guideline_data['pre_surgery_instructions'][:100]}...")
            print(f"- 禁食須知: {guideline_data['fasting_instructions'][:100]}...")
            print(f"- 藥物須知: {guideline_data['medication_instructions'][:100]}...")
            print(f"- 常見問題: {guideline_data['common_questions'][:100]}...")
            print(f"- 術後照護: {guideline_data['post_surgery_care'][:100]}...")
        else:
            print(f"錯誤: {response.text}")


async def test_get_patient_guidelines(patient_id):
    """測試獲取患者所有麻醉須知"""
    print("測試獲取患者所有麻醉須知...")
    
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/anesthesia/guidelines/patient/{patient_id}"
        response = await client.get(url)
        print(f"狀態碼: {response.status_code}")
        if response.status_code == 200:
            guidelines = response.json()
            print(f"患者共有 {len(guidelines)} 個麻醉須知")
            for guideline in guidelines:
                print(f"- {guideline['surgery_name']} ({guideline['surgery_date']})")
        else:
            print(f"錯誤: {response.text}")


async def test_health_check():
    """測試健康檢查"""
    print("測試健康檢查...")
    
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL.replace('/api/v1', '')}/health"
        response = await client.get(url)
        print(f"狀態碼: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"健康狀態: {health_data['status']}")
        else:
            print(f"錯誤: {response.text}")


async def main():
    """主函數"""
    print("開始 FastAPI 測試...")
    print("=" * 50)
    
    # 測試健康檢查
    await test_health_check()
    print("=" * 50)
    
    # 測試患者搜尋
    patient_id = await test_patient_search()
    if not patient_id:
        print("患者搜尋失敗，無法繼續測試")
        return
    
    print("=" * 50)
    
    # 測試生成麻醉須知
    guideline_id = await test_generate_guideline(patient_id)
    if not guideline_id:
        print("生成麻醉須知失敗，無法繼續測試")
        return
    
    print("=" * 50)
    
    # 測試獲取麻醉須知
    await test_get_guideline(guideline_id)
    
    print("=" * 50)
    
    # 測試獲取患者所有麻醉須知
    await test_get_patient_guidelines(patient_id)
    
    print("=" * 50)
    print("FastAPI 測試完成！")


if __name__ == '__main__':
    asyncio.run(main())