#!/usr/bin/env python3
"""
檢查醫療記錄數據
"""

import os
import sys
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.core.database import engine
from app.models.patient import MedicalHistory, SurgeryRecord

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_medical_data():
    """檢查醫療記錄數據"""
    db = SessionLocal()
    try:
        print("=== 檢查醫療記錄數據 ===")
        
        # 檢查醫療記錄
        print("\n醫療記錄:")
        for patient_id in [1, 2, 3]:
            print(f"\n患者 {patient_id}:")
            histories = db.query(MedicalHistory).filter(MedicalHistory.patient_id == patient_id).all()
            for h in histories:
                print(f"  - ID: {h.id}, 語言: {h.language}, Group ID: {h.group_id}, 過敏: {h.allergies[:30]}...")
        
        # 檢查手術記錄
        print("\n手術記錄:")
        for patient_id in [1, 2, 3]:
            print(f"\n患者 {patient_id}:")
            records = db.query(SurgeryRecord).filter(SurgeryRecord.patient_id == patient_id).all()
            for r in records:
                print(f"  - ID: {r.id}, 語言: {r.language}, Group ID: {r.group_id}, 手術: {r.surgery_name[:30]}...")
        
    except Exception as e:
        print(f"錯誤: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    check_medical_data()
