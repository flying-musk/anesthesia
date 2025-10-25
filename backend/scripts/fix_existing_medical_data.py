#!/usr/bin/env python3
"""
修復現有醫療數據，為沒有 group_id 的記錄添加 group_id 並創建多語言版本
"""

import os
import sys
import time
from datetime import date

# Add the parent directory to the Python path to allow imports from 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.core.database import get_db
from app.models.patient import MedicalHistory, SurgeryRecord
from app.schemas.patient import LanguageEnum

def fix_existing_medical_data():
    """修復現有的醫療數據，添加 group_id 並創建多語言版本"""
    db = next(get_db())
    
    try:
        print("=== 修復現有醫療數據 ===")
        
        # 1. 修復醫療病史記錄
        print("1. 修復醫療病史記錄...")
        
        # 找到所有沒有 group_id 的醫療病史記錄
        medical_histories_without_group = db.query(MedicalHistory).filter(
            MedicalHistory.group_id.is_(None)
        ).all()
        
        print(f"找到 {len(medical_histories_without_group)} 個需要修復的醫療病史記錄")
        
        for mh in medical_histories_without_group:
            # 為現有記錄添加 group_id
            group_id = int(time.time() * 1000)
            mh.group_id = group_id
            db.commit()
            
            print(f"✓ 為醫療病史 ID {mh.id} 添加 group_id: {group_id}")
            
            # 創建中文和法文版本
            for lang_code in ['zh', 'fr']:
                # 檢查是否已經存在該語言版本
                existing = db.query(MedicalHistory).filter(
                    MedicalHistory.patient_id == mh.patient_id,
                    MedicalHistory.group_id == group_id,
                    MedicalHistory.language == lang_code
                ).first()
                
                if not existing:
                    # 創建翻譯版本
                    translated_mh = MedicalHistory(
                        patient_id=mh.patient_id,
                        language=lang_code,
                        group_id=group_id,
                        allergies=f"[{lang_code.upper()}翻譯] {mh.allergies}" if mh.allergies else None,
                        chronic_conditions=f"[{lang_code.upper()}翻譯] {mh.chronic_conditions}" if mh.chronic_conditions else None,
                        current_medications=f"[{lang_code.upper()}翻譯] {mh.current_medications}" if mh.current_medications else None,
                        previous_surgeries=f"[{lang_code.upper()}翻譯] {mh.previous_surgeries}" if mh.previous_surgeries else None,
                        family_history=f"[{lang_code.upper()}翻譯] {mh.family_history}" if mh.family_history else None,
                        other_medical_info=f"[{lang_code.upper()}翻譯] {mh.other_medical_info}" if mh.other_medical_info else None,
                    )
                    db.add(translated_mh)
                    print(f"  ✓ 創建 {lang_code.upper()} 版本")
        
        db.commit()
        
        # 2. 修復手術記錄
        print("\n2. 修復手術記錄...")
        
        # 找到所有沒有 group_id 的手術記錄
        surgery_records_without_group = db.query(SurgeryRecord).filter(
            SurgeryRecord.group_id.is_(None)
        ).all()
        
        print(f"找到 {len(surgery_records_without_group)} 個需要修復的手術記錄")
        
        for sr in surgery_records_without_group:
            # 為現有記錄添加 group_id
            group_id = int(time.time() * 1000)
            sr.group_id = group_id
            db.commit()
            
            print(f"✓ 為手術記錄 ID {sr.id} 添加 group_id: {group_id}")
            
            # 創建中文和法文版本
            for lang_code in ['zh', 'fr']:
                # 檢查是否已經存在該語言版本
                existing = db.query(SurgeryRecord).filter(
                    SurgeryRecord.patient_id == sr.patient_id,
                    SurgeryRecord.group_id == group_id,
                    SurgeryRecord.language == lang_code
                ).first()
                
                if not existing:
                    # 創建翻譯版本
                    translated_sr = SurgeryRecord(
                        patient_id=sr.patient_id,
                        language=lang_code,
                        group_id=group_id,
                        surgery_name=sr.surgery_name,  # 手術名稱通常不需要翻譯
                        surgery_type=sr.surgery_type,  # 手術類型通常不需要翻譯
                        surgery_date=sr.surgery_date,
                        surgeon_name=sr.surgeon_name,  # 醫生姓名通常不需要翻譯
                        anesthesiologist_name=sr.anesthesiologist_name,  # 醫生姓名通常不需要翻譯
                        surgery_duration=sr.surgery_duration,
                        anesthesia_duration=sr.anesthesia_duration,
                        pre_surgery_assessment=f"[{lang_code.upper()}翻譯] {sr.pre_surgery_assessment}" if sr.pre_surgery_assessment else None,
                        post_surgery_notes=f"[{lang_code.upper()}翻譯] {sr.post_surgery_notes}" if sr.post_surgery_notes else None,
                        complications=f"[{lang_code.upper()}翻譯] {sr.complications}" if sr.complications else None,
                    )
                    db.add(translated_sr)
                    print(f"  ✓ 創建 {lang_code.upper()} 版本")
        
        db.commit()
        
        print("\n=== 修復完成 ===")
        
        # 驗證結果
        print("\n=== 驗證結果 ===")
        
        # 檢查醫療病史
        total_mh = db.query(MedicalHistory).count()
        mh_by_lang = {}
        for lang in ['en', 'zh', 'fr']:
            count = db.query(MedicalHistory).filter(MedicalHistory.language == lang).count()
            mh_by_lang[lang] = count
        
        print(f"醫療病史總數: {total_mh}")
        for lang, count in mh_by_lang.items():
            print(f"  {lang.upper()}: {count}")
        
        # 檢查手術記錄
        total_sr = db.query(SurgeryRecord).count()
        sr_by_lang = {}
        for lang in ['en', 'zh', 'fr']:
            count = db.query(SurgeryRecord).filter(SurgeryRecord.language == lang).count()
            sr_by_lang[lang] = count
        
        print(f"\n手術記錄總數: {total_sr}")
        for lang, count in sr_by_lang.items():
            print(f"  {lang.upper()}: {count}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 修復失敗: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_existing_medical_data()
