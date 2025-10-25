#!/usr/bin/env python3
"""
Test script for medical multilingual functionality
"""

import os
import sys
import asyncio
from datetime import date

# Add the parent directory to the Python path to allow imports from 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.core.database import get_db
from app.models.patient import Patient, MedicalHistory, SurgeryRecord
from app.schemas.patient import MedicalHistoryCreate, SurgeryRecordCreate, LanguageEnum
from app.services.medical_multilingual_service import medical_multilingual_service

async def test_medical_multilingual():
    """Test multilingual medical history and surgery records"""
    db = next(get_db())

    try:
        print("=== Testing Medical Multilingual Functionality ===")

        # Get a test patient
        patient = db.query(Patient).first()
        if not patient:
            print("❌ No patients found. Please run init_sample_data.py first.")
            return

        print(f"Using patient: {patient.full_name} (ID: {patient.id})")

        # Test 1: Create multilingual medical history
        print("\n1. Testing multilingual medical history creation...")

        medical_history_data = MedicalHistoryCreate(
            patient_id=patient.id,
            allergies="Penicillin allergy",
            chronic_conditions="Hypertension",
            current_medications="Lisinopril 10mg daily",
            previous_surgeries="Appendectomy in 2000",
            family_history="Father had heart disease",
            other_medical_info="Regular checkups, stable condition."
        )

        medical_histories = await medical_multilingual_service.create_medical_history_multilingual(
            db, patient.id, medical_history_data
        )

        print(f"✅ Created {len(medical_histories)} medical history records")
        for mh in medical_histories:
            print(f"   - Language: {mh.language}, Group ID: {mh.group_id}")

        # Test 2: Create multilingual surgery record
        print("\n2. Testing multilingual surgery record creation...")

        surgery_record_data = SurgeryRecordCreate(
            patient_id=patient.id,
            surgery_name="Cataract surgery",
            surgery_type="regional",
            surgery_date=date(2025, 1, 15),
            surgeon_name="Dr. Michael Chen",
            anesthesiologist_name="Dr. Robert Taylor",
            surgery_duration=120,
            anesthesia_duration=90,
            pre_surgery_assessment="Patient assessed for cataract surgery. Vital signs stable.",
            post_surgery_notes="Patient recovered well. No complications noted.",
            complications="None"
        )

        surgery_records = await medical_multilingual_service.create_surgery_record_multilingual(
            db, patient.id, surgery_record_data
        )

        print(f"✅ Created {len(surgery_records)} surgery record entries")
        for sr in surgery_records:
            print(f"   - Language: {sr.language}, Group ID: {sr.group_id}")

        # Test 3: Verify language-specific retrieval
        print("\n3. Testing language-specific retrieval...")

        # Get medical history in different languages
        for lang in [LanguageEnum.EN, LanguageEnum.ZH, LanguageEnum.FR, LanguageEnum.ES, LanguageEnum.JA, LanguageEnum.KO]:
            mh = db.query(MedicalHistory).filter(
                MedicalHistory.patient_id == patient.id,
                MedicalHistory.language == lang.value
            ).first()

            if mh:
                print(f"✅ Found medical history in {lang.value.upper()}: {mh.chronic_conditions}")
            else:
                print(f"❌ No medical history found in {lang.value.upper()}")

        # Get surgery records in different languages
        for lang in [LanguageEnum.EN, LanguageEnum.ZH, LanguageEnum.FR, LanguageEnum.ES, LanguageEnum.JA, LanguageEnum.KO]:
            sr_count = db.query(SurgeryRecord).filter(
                SurgeryRecord.patient_id == patient.id,
                SurgeryRecord.language == lang.value
            ).count()

            print(f"✅ Found {sr_count} surgery records in {lang.value.upper()}")

        print("\n=== Test Complete ===")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_medical_multilingual())
