#!/usr/bin/env python
"""
快速啟動腳本 - 用於 hackathon demo
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db
from app.models.patient import Patient, MedicalHistory, SurgeryRecord
from app.models.anesthesia import AnesthesiaGuidelineTemplate
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from datetime import date


async def create_demo_data():
    """建立 demo 資料"""
    print("建立 demo 資料...")
    
    db = SessionLocal()
    try:
        # 檢查是否已有資料
        if db.query(Patient).count() > 0:
            print("資料已存在，跳過建立")
            return
        
        # 建立患者 1
        patient1 = Patient(
            health_insurance_number='1234567890',
            full_name='王小明',
            date_of_birth=date(1985, 5, 15),
            gender='M',
            phone_number='0912345678',
            emergency_contact_name='王大明',
            emergency_contact_relationship='配偶',
            emergency_contact_phone='0912345679'
        )
        
        db.add(patient1)
        db.commit()
        db.refresh(patient1)
        
        # 建立患者 1 的醫療病史
        medical_history1 = MedicalHistory(
            patient_id=patient1.id,
            allergies='青黴素過敏',
            chronic_conditions='高血壓',
            current_medications='降血壓藥物',
            previous_surgeries='闌尾切除術 (2010年)',
            family_history='父親有糖尿病史'
        )
        
        db.add(medical_history1)
        
        # 建立患者 2
        patient2 = Patient(
            health_insurance_number='0987654321',
            full_name='李小華',
            date_of_birth=date(1990, 8, 22),
            gender='F',
            phone_number='0987654321',
            emergency_contact_name='李大明',
            emergency_contact_relationship='父親',
            emergency_contact_phone='0987654322'
        )
        
        db.add(patient2)
        db.commit()
        db.refresh(patient2)
        
        # 建立患者 2 的醫療病史
        medical_history2 = MedicalHistory(
            patient_id=patient2.id,
            allergies='無',
            chronic_conditions='無',
            current_medications='無',
            previous_surgeries='無',
            family_history='母親有乳癌病史'
        )
        
        db.add(medical_history2)
        
        # 建立麻醉模板
        template1 = AnesthesiaGuidelineTemplate(
            template_name='標準全身麻醉模板',
            anesthesia_type='general',
            anesthesia_type_template='全身麻醉是讓您在手術過程中完全失去意識的麻醉方式。麻醉醫師會通過靜脈注射和氣體麻醉來確保您在手術期間完全無意識。',
            surgery_process_template='手術將在您完全無意識的狀態下進行。麻醉醫師會全程監控您的生命徵象，確保手術安全進行。',
            expected_sensations_template='您將不會感受到任何疼痛或不適。手術結束後，您會逐漸恢復意識，可能會感到輕微的頭暈或噁心。',
            potential_risks_template='可能包括：噁心、嘔吐、喉嚨痛、頭暈、肌肉疼痛等。嚴重併發症極為罕見，包括過敏反應、呼吸問題等。',
            pre_surgery_template='請按照醫師指示進行術前準備，包括禁食禁水、停用特定藥物等。',
            fasting_template='手術前8小時開始禁食，2小時前禁水。這是為了避免麻醉時發生嘔吐和吸入性肺炎的風險。',
            medication_template='請告知醫師您目前服用的所有藥物。某些藥物（如抗凝血劑）可能需要提前停用。',
            common_questions_template='Q: 麻醉會不會有副作用？\nA: 大多數患者只會有輕微的副作用，如噁心、頭暈等，通常24小時內會消失。',
            post_surgery_template='術後請按照醫師指示進行照護，包括傷口護理、藥物服用、活動限制等。如有異常請立即就醫。'
        )
        
        db.add(template1)
        db.commit()
        
        print("✅ Demo 資料建立完成！")
        print(f"📊 已建立 {db.query(Patient).count()} 位患者")
        print(f"📋 已建立 {db.query(AnesthesiaGuidelineTemplate).count()} 個模板")
        print("\n🎯 Demo 患者資訊：")
        print("患者1: 王小明 (健保號: 1234567890)")
        print("患者2: 李小華 (健保號: 0987654321)")
        
    finally:
        db.close()


async def main():
    """主函數"""
    print("🚀 啟動麻醉前須知生成系統 Demo...")
    print("=" * 50)
    
    # 初始化資料庫
    print("📁 初始化 SQLite 資料庫...")
    await init_db()
    print("✅ 資料庫初始化完成")
    
    # 建立 demo 資料
    await create_demo_data()
    
    print("=" * 50)
    print("🎉 系統準備完成！")
    print("\n📖 使用說明：")
    print("1. 啟動伺服器: uvicorn app.main:app --reload")
    print("2. 查看 API 文檔: http://localhost:8000/docs")
    print("3. 測試 API: python scripts/test_api.py")
    print("\n🔍 Demo 患者搜尋範例：")
    print("健保號: 1234567890")
    print("姓名: 王小明")
    print("生日: 1985-05-15")


if __name__ == '__main__':
    asyncio.run(main())
