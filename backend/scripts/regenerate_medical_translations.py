#!/usr/bin/env python3
"""
重新生成醫療記錄的翻譯
"""

import os
import sys
import asyncio
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.core.database import engine
from app.models.patient import MedicalHistory, SurgeryRecord
from app.services.medical_multilingual_service import medical_multilingual_service
from app.schemas.patient import LanguageEnum

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def regenerate_medical_translations():
    """重新生成醫療記錄的翻譯"""
    db = SessionLocal()
    try:
        print("=== 重新生成醫療記錄翻譯 ===")
        
        # 獲取所有英文版本的醫療記錄
        english_medical_histories = db.query(MedicalHistory).filter(
            MedicalHistory.language == "en"
        ).all()
        
        print(f"找到 {len(english_medical_histories)} 個英文醫療記錄")
        
        for mh in english_medical_histories:
            print(f"\n處理醫療記錄 ID: {mh.id}, 患者 ID: {mh.patient_id}")
            
            # 刪除現有的中文和法文版本
            db.query(MedicalHistory).filter(
                MedicalHistory.patient_id == mh.patient_id,
                MedicalHistory.group_id == mh.group_id,
                MedicalHistory.language.in_(["zh", "fr"])
            ).delete()
            
            # 重新生成翻譯
            from app.schemas.patient import MedicalHistoryCreate
            
            # 創建英文版本的數據
            english_data = {
                "allergies": mh.allergies,
                "chronic_conditions": mh.chronic_conditions,
                "current_medications": mh.current_medications,
                "previous_surgeries": mh.previous_surgeries,
                "family_history": mh.family_history,
                "other_medical_info": mh.other_medical_info,
                "language": LanguageEnum.EN
            }
            
            mh_create = MedicalHistoryCreate(**english_data)
            
            # 重新生成多語言版本
            new_histories = await medical_multilingual_service.create_medical_history_multilingual(
                db, mh.patient_id, mh_create
            )
            
            print(f"  重新生成了 {len(new_histories)} 個語言版本")
            for history in new_histories:
                print(f"    - 語言: {history.language}, 過敏: {history.allergies[:30]}...")
        
        # 獲取所有英文版本的手術記錄
        english_surgery_records = db.query(SurgeryRecord).filter(
            SurgeryRecord.language == "en"
        ).all()
        
        print(f"\n找到 {len(english_surgery_records)} 個英文手術記錄")
        
        for sr in english_surgery_records:
            print(f"\n處理手術記錄 ID: {sr.id}, 患者 ID: {sr.patient_id}")
            
            # 刪除現有的中文和法文版本
            db.query(SurgeryRecord).filter(
                SurgeryRecord.patient_id == sr.patient_id,
                SurgeryRecord.group_id == sr.group_id,
                SurgeryRecord.language.in_(["zh", "fr"])
            ).delete()
            
            # 重新生成翻譯
            from app.schemas.patient import SurgeryRecordCreate
            
            # 創建英文版本的數據
            english_data = {
                "surgery_name": sr.surgery_name,
                "surgery_type": sr.surgery_type,
                "surgery_date": sr.surgery_date,
                "surgeon_name": sr.surgeon_name,
                "anesthesiologist_name": sr.anesthesiologist_name,
                "surgery_duration": sr.surgery_duration,
                "anesthesia_duration": sr.anesthesia_duration,
                "pre_surgery_assessment": sr.pre_surgery_assessment,
                "post_surgery_notes": sr.post_surgery_notes,
                "complications": sr.complications,
                "language": LanguageEnum.EN
            }
            
            sr_create = SurgeryRecordCreate(**english_data)
            
            # 重新生成多語言版本
            new_records = await medical_multilingual_service.create_surgery_record_multilingual(
                db, sr.patient_id, sr_create
            )
            
            print(f"  重新生成了 {len(new_records)} 個語言版本")
            for record in new_records:
                print(f"    - 語言: {record.language}, 手術名稱: {record.surgery_name[:30]}...")
        
        db.commit()
        print("\n=== 重新生成完成 ===")
        
    except Exception as e:
        db.rollback()
        print(f"錯誤: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(regenerate_medical_translations())
