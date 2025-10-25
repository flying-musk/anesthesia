#!/usr/bin/env python3
"""
完整系統測試腳本
測試前端和後端的整合
"""

import requests
import json
import time

# API基礎URL
BASE_URL = 'http://localhost:8000/api/v1'

def test_backend_health():
    """測試後端健康狀態"""
    print("🔍 測試後端健康狀態...")
    try:
        response = requests.get('http://localhost:8000/health')
        if response.status_code == 200:
            print("✅ 後端服務正常運行")
            return True
        else:
            print(f"❌ 後端服務異常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 無法連接到後端: {str(e)}")
        return False

def test_patient_api():
    """測試患者API"""
    print("\n👥 測試患者API...")
    try:
        # 獲取患者列表
        response = requests.get(f'{BASE_URL}/patients/')
        if response.status_code == 200:
            patients = response.json()
            print(f"✅ 獲取患者列表成功，共 {len(patients)} 位患者")
            if patients:
                return patients[0]['id']  # 返回第一個患者的ID
            else:
                print("⚠️ 沒有找到患者，請先運行 start_demo.py")
                return None
        else:
            print(f"❌ 獲取患者列表失敗: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 患者API測試失敗: {str(e)}")
        return None

def test_anesthesia_generate(patient_id):
    """測試麻醉須知生成API"""
    print(f"\n💊 測試麻醉須知生成API (患者ID: {patient_id})...")
    try:
        data = {
            "patient_id": patient_id,
            "surgery_name": "Laparoscopic Cholecystectomy",
            "anesthesia_type": "general",
            "surgery_date": "2025-10-25T07:00:00.000Z",  # 測試datetime格式
            "surgeon_name": "Dr. Smith",
            "anesthesiologist_name": "Dr. Johnson"
        }
        
        response = requests.post(f'{BASE_URL}/anesthesia/guidelines/generate', json=data)
        if response.status_code == 201:
            guideline = response.json()
            print("✅ 麻醉須知生成成功！")
            print(f"📋 手術名稱: {guideline['surgery_name']}")
            print(f"🏥 麻醉類型: {guideline['anesthesia_type']}")
            print(f"📅 手術日期: {guideline['surgery_date']}")
            print(f"🤖 AI生成: {guideline['is_generated']}")
            return guideline['id']
        else:
            print(f"❌ 麻醉須知生成失敗: {response.status_code}")
            print(f"錯誤詳情: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 麻醉須知生成測試失敗: {str(e)}")
        return None

def test_guideline_details(guideline_id):
    """測試麻醉須知詳情API"""
    print(f"\n📄 測試麻醉須知詳情API (ID: {guideline_id})...")
    try:
        response = requests.get(f'{BASE_URL}/anesthesia/guidelines/{guideline_id}')
        if response.status_code == 200:
            guideline = response.json()
            print("✅ 獲取麻醉須知詳情成功！")
            print(f"📝 麻醉類型說明: {guideline['anesthesia_type_info'][:50]}...")
            print(f"🔬 手術過程: {guideline['surgery_process'][:50]}...")
            print(f"⚠️ 可能風險: {guideline['potential_risks'][:50]}...")
            return True
        else:
            print(f"❌ 獲取麻醉須知詳情失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 麻醉須知詳情測試失敗: {str(e)}")
        return False

def test_frontend_connection():
    """測試前端連接"""
    print("\n🎨 測試前端連接...")
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✅ 前端服務正常運行")
            return True
        else:
            print(f"❌ 前端服務異常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 無法連接到前端: {str(e)}")
        print("💡 請確保前端服務正在運行: cd frontend && npm start")
        return False

def main():
    """主函數"""
    print("🚀 完整系統測試開始...")
    print("=" * 50)
    
    # 測試後端健康狀態
    if not test_backend_health():
        print("\n❌ 後端測試失敗，請先啟動後端服務")
        return
    
    # 測試患者API
    patient_id = test_patient_api()
    if not patient_id:
        print("\n❌ 患者API測試失敗")
        return
    
    # 測試麻醉須知生成
    guideline_id = test_anesthesia_generate(patient_id)
    if not guideline_id:
        print("\n❌ 麻醉須知生成測試失敗")
        return
    
    # 測試麻醉須知詳情
    if not test_guideline_details(guideline_id):
        print("\n❌ 麻醉須知詳情測試失敗")
        return
    
    # 測試前端連接
    frontend_ok = test_frontend_connection()
    
    print("\n" + "=" * 50)
    print("🎉 系統測試完成！")
    print("\n📊 測試結果:")
    print("✅ 後端服務正常")
    print("✅ 患者API正常")
    print("✅ 麻醉須知生成正常")
    print("✅ 麻醉須知詳情正常")
    
    if frontend_ok:
        print("✅ 前端服務正常")
        print("\n🌐 訪問地址:")
        print("  - 前端界面: http://localhost:3000")
        print("  - API文檔: http://localhost:8000/docs")
        print("  - 健康檢查: http://localhost:8000/health")
    else:
        print("⚠️ 前端服務未運行")
        print("\n💡 啟動前端: cd frontend && npm start")
    
    print("\n🎯 系統功能:")
    print("  - ✅ 患者管理")
    print("  - ✅ 醫療病史管理")
    print("  - ✅ AI麻醉須知生成")
    print("  - ✅ 多語言支援 (中文/英文/法文)")
    print("  - ✅ 現代化UI界面")

if __name__ == "__main__":
    main()
