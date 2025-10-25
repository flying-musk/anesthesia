#!/usr/bin/env python3
"""
重新生成手術記錄的翻譯
"""

import os
import sys
import asyncio
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.core.database import engine
from app.models.patient import SurgeryRecord
from app.services.medical_multilingual_service import medical_multilingual_service
from app.schemas.patient import LanguageEnum

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def regenerate_surgery_translations():
    """重新生成手術記錄的翻譯"""
    db = SessionLocal()
    try:
        print("=== 重新生成手術記錄翻譯 ===")
        
        # 獲取所有英文版本的手術記錄
        english_surgery_records = db.query(SurgeryRecord).filter(
            SurgeryRecord.language == "en"
        ).all()
        
        print(f"找到 {len(english_surgery_records)} 個英文手術記錄")
        
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
    asyncio.run(regenerate_surgery_translations())
