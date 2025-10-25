#!/usr/bin/env python3
"""
Complete Multilingual System Initialization Script
This script initializes the entire system with multilingual support for:
- Anesthesia guidelines (EN/ZH/FR)
- Medical history (EN/ZH/FR) 
- Surgery records (EN/ZH/FR)
- Sample patients with complete multilingual data
"""

import os
import sys
import asyncio
import time
from datetime import date, datetime, timedelta
from random import choice, randint

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from app.core.database import engine, Base
from app.models.patient import Patient, MedicalHistory, SurgeryRecord
from app.models.anesthesia import AnesthesiaGuideline, AnesthesiaGuidelineTemplate
from app.schemas.patient import MedicalHistoryCreate, SurgeryRecordCreate, LanguageEnum
from app.services.medical_multilingual_service import medical_multilingual_service
from app.services.anesthesia_service import AnesthesiaGuidelineService

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def run_database_migrations():
    """Run all necessary database migrations"""
    print("=== Running Database Migrations ===")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Add language column to anesthesia_guidelines if not exists
    try:
        with engine.connect() as conn:
            conn.execute("""
                ALTER TABLE anesthesia_guidelines
                ADD COLUMN language VARCHAR(10) NOT NULL DEFAULT 'en'
            """)
            print("✅ Added language column to anesthesia_guidelines")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("✅ Language column already exists in anesthesia_guidelines")
        else:
            print(f"⚠️  Warning: {e}")
    
    # Add group_id column to anesthesia_guidelines if not exists
    try:
        with engine.connect() as conn:
            conn.execute("""
                ALTER TABLE anesthesia_guidelines
                ADD COLUMN group_id INTEGER
            """)
            print("✅ Added group_id column to anesthesia_guidelines")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("✅ Group_id column already exists in anesthesia_guidelines")
        else:
            print(f"⚠️  Warning: {e}")
    
    # Add language and group_id columns to medical_histories if not exists
    try:
        with engine.connect() as conn:
            conn.execute("""
                ALTER TABLE medical_histories
                ADD COLUMN language VARCHAR(10) NOT NULL DEFAULT 'en'
            """)
            print("✅ Added language column to medical_histories")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("✅ Language column already exists in medical_histories")
        else:
            print(f"⚠️  Warning: {e}")
    
    try:
        with engine.connect() as conn:
            conn.execute("""
                ALTER TABLE medical_histories
                ADD COLUMN group_id INTEGER
            """)
            print("✅ Added group_id column to medical_histories")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("✅ Group_id column already exists in medical_histories")
        else:
            print(f"⚠️  Warning: {e}")
    
    # Add language and group_id columns to surgery_records if not exists
    try:
        with engine.connect() as conn:
            conn.execute("""
                ALTER TABLE surgery_records
                ADD COLUMN language VARCHAR(10) NOT NULL DEFAULT 'en'
            """)
            print("✅ Added language column to surgery_records")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("✅ Language column already exists in surgery_records")
        else:
            print(f"⚠️  Warning: {e}")
    
    try:
        with engine.connect() as conn:
            conn.execute("""
                ALTER TABLE surgery_records
                ADD COLUMN group_id INTEGER
            """)
            print("✅ Added group_id column to surgery_records")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("✅ Group_id column already exists in surgery_records")
        else:
            print(f"⚠️  Warning: {e}")

async def create_anesthesia_templates():
    """Create anesthesia guideline templates in multiple languages"""
    print("\n=== Creating Anesthesia Templates ===")
    
    db = SessionLocal()
    try:
        # Check if templates already exist
        existing_templates = db.query(AnesthesiaGuidelineTemplate).count()
        if existing_templates > 0:
            print(f"✅ {existing_templates} anesthesia templates already exist")
            return
        
        # General anesthesia template
        template1 = AnesthesiaGuidelineTemplate(
            template_name='Standard General Anesthesia Template',
            anesthesia_type='general',
            anesthesia_type_template='General anesthesia is a method that makes you completely unconscious during surgery. The anesthesiologist will ensure you are completely unconscious during the operation through intravenous injection and gas anesthesia.',
            surgery_process_template='The surgery will be performed while you are completely unconscious. The anesthesiologist will monitor your vital signs throughout to ensure the surgery proceeds safely.',
            expected_sensations_template='You will not feel any pain or discomfort. After the surgery, you will gradually regain consciousness and may feel mild dizziness or nausea.',
            potential_risks_template='May include: nausea, vomiting, sore throat, dizziness, muscle pain, etc. Serious complications are extremely rare, including allergic reactions, breathing problems, etc.',
            pre_surgery_template='Please prepare for surgery according to your doctor\'s instructions, including fasting, stopping certain medications, etc.',
            fasting_template='Begin fasting 8 hours before surgery, no water 2 hours before. This is to avoid the risk of vomiting and aspiration pneumonia during anesthesia.',
            medication_template='Please inform your doctor of all medications you are currently taking. Some medications (such as anticoagulants) may need to be discontinued in advance.',
            common_questions_template='Q: Will anesthesia have side effects?\nA: Most patients only have mild side effects, such as nausea and dizziness, which usually disappear within 24 hours.',
            post_surgery_template='After surgery, please follow your doctor\'s instructions for care, including wound care, medication, activity restrictions, etc. Seek medical attention immediately if any abnormalities occur.'
        )
        
        db.add(template1)
        
        # Local anesthesia template
        template2 = AnesthesiaGuidelineTemplate(
            template_name='Standard Local Anesthesia Template',
            anesthesia_type='local',
            anesthesia_type_template='Local anesthesia numbs only the surgical area, allowing you to remain awake during the procedure.',
            surgery_process_template='You will remain awake during the surgery, but the surgical area will not feel pain.',
            expected_sensations_template='The surgical area will feel numb but not painful. You may feel touch or pressure but no pain.',
            potential_risks_template='May include: pain at injection site, bruising, infection, etc. Serious complications are extremely rare.',
            pre_surgery_template='Please prepare for surgery according to your doctor\'s instructions.',
            fasting_template='Fasting is usually not required, but please follow your doctor\'s instructions.',
            medication_template='Please inform your doctor of all medications you are currently taking.',
            common_questions_template='Q: Will local anesthesia hurt?\nA: There will be a slight sting during injection, but it will quickly become numb.',
            post_surgery_template='After surgery, please follow your doctor\'s instructions for care. The anesthetic effect usually lasts several hours.'
        )
        
        db.add(template2)
        
        # Regional anesthesia template
        template3 = AnesthesiaGuidelineTemplate(
            template_name='Standard Regional Anesthesia Template',
            anesthesia_type='regional',
            anesthesia_type_template='Regional anesthesia blocks sensation in a larger area of your body, such as an entire limb or the lower half of your body.',
            surgery_process_template='You will remain awake during the surgery, but the anesthetized area will not feel pain.',
            expected_sensations_template='The anesthetized area will feel numb. You may feel touch or pressure but no pain in the blocked area.',
            potential_risks_template='May include: headache, back pain, difficulty urinating, etc. Serious complications are rare.',
            pre_surgery_template='Please prepare for surgery according to your doctor\'s instructions.',
            fasting_template='Follow your doctor\'s specific fasting instructions.',
            medication_template='Please inform your doctor of all medications you are currently taking.',
            common_questions_template='Q: How long will the numbness last?\nA: The numbness typically lasts several hours, depending on the type of regional anesthesia used.',
            post_surgery_template='After surgery, the numbness will gradually wear off. Follow your doctor\'s instructions for care and activity restrictions.'
        )
        
        db.add(template3)
        
        # Sedation anesthesia template
        template4 = AnesthesiaGuidelineTemplate(
            template_name='Standard Sedation Anesthesia Template',
            anesthesia_type='sedation',
            anesthesia_type_template='Sedation anesthesia makes you drowsy and relaxed, but you may not remember the procedure clearly.',
            surgery_process_template='You will be in a relaxed, sleepy state during the procedure. The anesthesiologist will monitor your breathing and vital signs.',
            expected_sensations_template='You will feel very drowsy and relaxed. You may not remember much of the procedure afterward.',
            potential_risks_template='May include: nausea, dizziness, memory loss, breathing difficulties, etc. Serious complications are rare.',
            pre_surgery_template='Please prepare for surgery according to your doctor\'s instructions.',
            fasting_template='Begin fasting 6 hours before surgery, no water 2 hours before.',
            medication_template='Please inform your doctor of all medications you are currently taking.',
            common_questions_template='Q: Will I remember the procedure?\nA: You may have little or no memory of the procedure due to the sedative effects.',
            post_surgery_template='After surgery, you will gradually become more alert. You may feel drowsy for several hours. Arrange for someone to drive you home.'
        )
        
        db.add(template4)
        
        db.commit()
        print(f"✅ Created {db.query(AnesthesiaGuidelineTemplate).count()} anesthesia templates")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating anesthesia templates: {e}")
        raise
    finally:
        db.close()

async def create_multilingual_sample_patients():
    """Create sample patients with complete multilingual data"""
    print("\n=== Creating Multilingual Sample Patients ===")
    
    db = SessionLocal()
    try:
        # Sample patients data
        patients_data = [
            {
                "health_insurance_number": "1234567890",
                "full_name": "John Smith",
                "date_of_birth": date(1985, 5, 15),
                "gender": "M",
                "phone_number": "555-0123",
                "emergency_contact_name": "Jane Smith",
                "emergency_contact_relationship": "Spouse",
                "emergency_contact_phone": "555-0124",
            },
            {
                "health_insurance_number": "0987654321",
                "full_name": "Emily Johnson",
                "date_of_birth": date(1990, 8, 22),
                "gender": "F",
                "phone_number": "555-4321",
                "emergency_contact_name": "Robert Johnson",
                "emergency_contact_relationship": "Father",
                "emergency_contact_phone": "555-4322",
            },
            {
                "health_insurance_number": "1122334455",
                "full_name": "Michael Chen",
                "date_of_birth": date(1988, 3, 10),
                "gender": "M",
                "phone_number": "555-7890",
                "emergency_contact_name": "Sarah Chen",
                "emergency_contact_relationship": "Wife",
                "emergency_contact_phone": "555-7891",
            }
        ]
        
        patient_objects = []
        for p_data in patients_data:
            # Check if patient already exists
            existing_patient = db.query(Patient).filter(
                Patient.health_insurance_number == p_data["health_insurance_number"]
            ).first()
            
            if not existing_patient:
                patient = Patient(**p_data)
                db.add(patient)
                db.commit()
                db.refresh(patient)
                print(f"✅ Created patient: {patient.full_name}")
            else:
                patient = existing_patient
                print(f"✅ Patient already exists: {patient.full_name}")
            
            patient_objects.append(patient)
        
        # Create multilingual medical histories
        medical_histories_data = {
            "John Smith": {
                "allergies": "Penicillin allergy",
                "chronic_conditions": "Hypertension",
                "current_medications": "Blood pressure medication",
                "previous_surgeries": "Appendectomy (2010)",
                "family_history": "Father has diabetes",
                "other_medical_info": "Patient has been stable with current medications. Regular checkups every 3 months.",
                "language": LanguageEnum.EN
            },
            "Emily Johnson": {
                "allergies": "Latex allergy",
                "chronic_conditions": "Asthma",
                "current_medications": "Albuterol inhaler as needed",
                "previous_surgeries": "Tonsillectomy (2015)",
                "family_history": "Mother has breast cancer history",
                "other_medical_info": "Well-controlled asthma. Uses inhaler before exercise.",
                "language": LanguageEnum.EN
            },
            "Michael Chen": {
                "allergies": "Shellfish allergy",
                "chronic_conditions": "Diabetes Type 2",
                "current_medications": "Metformin 500mg daily",
                "previous_surgeries": "Gallbladder removal (2020)",
                "family_history": "Both parents have diabetes",
                "other_medical_info": "Diabetes well-controlled with medication. Regular blood sugar monitoring.",
                "language": LanguageEnum.EN
            }
        }
        
        for patient in patient_objects:
            print(f"\n--- Creating multilingual medical history for {patient.full_name} ---")
            mh_data = medical_histories_data.get(patient.full_name)
            if mh_data:
                # Check if medical history already exists
                existing_mh = db.query(MedicalHistory).filter(
                    MedicalHistory.patient_id == patient.id
                ).first()
                
                if not existing_mh:
                    mh_create = MedicalHistoryCreate(**mh_data)
                    await medical_multilingual_service.create_medical_history_multilingual(
                        db, patient.id, mh_create
                    )
                    print(f"✅ Created medical history for {patient.full_name} in all languages")
                else:
                    print(f"✅ Medical history already exists for {patient.full_name}")
        
        # Create multilingual surgery records
        surgery_records_data = {
            "John Smith": [
                {
                    "surgery_name": "Cataract surgery",
                    "surgery_type": "local",
                    "surgery_date": date(2024, 6, 15),
                    "surgeon_name": "Dr. Maria Garcia",
                    "anesthesiologist_name": "Dr. Robert Taylor",
                    "surgery_duration": 90,
                    "anesthesia_duration": 120,
                    "pre_surgery_assessment": "Patient assessed for cataract surgery. Vital signs stable. No contraindications for local anesthesia.",
                    "post_surgery_notes": "Patient recovered well from cataract surgery. No complications noted. Discharged same day.",
                    "complications": "None",
                    "language": LanguageEnum.EN
                },
                {
                    "surgery_name": "Gallbladder removal",
                    "surgery_type": "general",
                    "surgery_date": date(2023, 12, 10),
                    "surgeon_name": "Dr. Michael Chen",
                    "anesthesiologist_name": "Dr. Sarah Johnson",
                    "surgery_duration": 120,
                    "anesthesia_duration": 150,
                    "pre_surgery_assessment": "Patient assessed for gallbladder removal. Vital signs stable. No contraindications for general anesthesia.",
                    "post_surgery_notes": "Patient recovered well from gallbladder removal. No complications noted. Discharged after 2 days.",
                    "complications": "None",
                    "language": LanguageEnum.EN
                }
            ],
            "Emily Johnson": [
                {
                    "surgery_name": "Tonsillectomy",
                    "surgery_type": "general",
                    "surgery_date": date(2015, 8, 20),
                    "surgeon_name": "Dr. Lisa Wang",
                    "anesthesiologist_name": "Dr. Christopher Brown",
                    "surgery_duration": 45,
                    "anesthesia_duration": 60,
                    "pre_surgery_assessment": "Patient assessed for tonsillectomy. Vital signs stable. No contraindications for general anesthesia.",
                    "post_surgery_notes": "Patient recovered well from tonsillectomy. No complications noted. Discharged same day.",
                    "complications": "None",
                    "language": LanguageEnum.EN
                }
            ],
            "Michael Chen": [
                {
                    "surgery_name": "Gallbladder removal",
                    "surgery_type": "general",
                    "surgery_date": date(2020, 11, 5),
                    "surgeon_name": "Dr. David Lee",
                    "anesthesiologist_name": "Dr. Maria Garcia",
                    "surgery_duration": 110,
                    "anesthesia_duration": 140,
                    "pre_surgery_assessment": "Patient assessed for gallbladder removal. Vital signs stable. No contraindications for general anesthesia.",
                    "post_surgery_notes": "Patient recovered well from gallbladder removal. No complications noted. Discharged after 1 day.",
                    "complications": "None",
                    "language": LanguageEnum.EN
                },
                {
                    "surgery_name": "Appendectomy",
                    "surgery_type": "general",
                    "surgery_date": date(2018, 4, 12),
                    "surgeon_name": "Dr. Robert Taylor",
                    "anesthesiologist_name": "Dr. Sarah Johnson",
                    "surgery_duration": 75,
                    "anesthesia_duration": 90,
                    "pre_surgery_assessment": "Patient assessed for appendectomy. Vital signs stable. No contraindications for general anesthesia.",
                    "post_surgery_notes": "Patient recovered well from appendectomy. No complications noted. Discharged after 2 days.",
                    "complications": "None",
                    "language": LanguageEnum.EN
                }
            ]
        }
        
        for patient in patient_objects:
            print(f"\n--- Creating multilingual surgery records for {patient.full_name} ---")
            sr_list = surgery_records_data.get(patient.full_name, [])
            for i, sr_data in enumerate(sr_list):
                # Check if surgery record already exists
                existing_sr = db.query(SurgeryRecord).filter(
                    SurgeryRecord.patient_id == patient.id,
                    SurgeryRecord.surgery_name == sr_data["surgery_name"],
                    SurgeryRecord.surgery_date == sr_data["surgery_date"]
                ).first()
                
                if not existing_sr:
                    sr_create = SurgeryRecordCreate(**sr_data)
                    await medical_multilingual_service.create_surgery_record_multilingual(
                        db, patient.id, sr_create
                    )
                    print(f"✅ Created surgery record {i+1} in all languages")
                else:
                    print(f"✅ Surgery record {i+1} already exists for {patient.full_name}")
        
        db.commit()
        print("\n=== Multilingual Sample Data Creation Complete ===")
        
        # Verification
        total_patients = db.query(Patient).count()
        total_medical_histories = db.query(MedicalHistory).count()
        total_surgery_records = db.query(SurgeryRecord).count()
        
        print(f"\n=== Data Summary ===")
        print(f"Total patients: {total_patients}")
        print(f"Total medical histories: {total_medical_histories}")
        print(f"Total surgery records: {total_surgery_records}")
        
        print(f"\n=== Language Distribution ===")
        for lang in [LanguageEnum.EN, LanguageEnum.ZH, LanguageEnum.FR]:
            mh_count = db.query(MedicalHistory).filter(MedicalHistory.language == lang.value).count()
            sr_count = db.query(SurgeryRecord).filter(SurgeryRecord.language == lang.value).count()
            print(f"{lang.value.upper()}: {mh_count} medical histories, {sr_count} surgery records")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating sample data: {e}")
        raise
    finally:
        db.close()

async def create_sample_anesthesia_guidelines():
    """Create sample anesthesia guidelines in multiple languages"""
    print("\n=== Creating Sample Anesthesia Guidelines ===")
    
    db = SessionLocal()
    try:
        # Check if guidelines already exist
        existing_guidelines = db.query(AnesthesiaGuideline).count()
        if existing_guidelines > 0:
            print(f"✅ {existing_guidelines} anesthesia guidelines already exist")
            return
        
        # Get a patient to create guidelines for
        patient = db.query(Patient).first()
        if not patient:
            print("⚠️  No patients found, skipping anesthesia guidelines creation")
            return
        
        # Create sample guidelines using the service
        from app.schemas.anesthesia import GenerateGuidelineRequest
        
        anesthesia_service = AnesthesiaGuidelineService()
        
        # Create a general anesthesia guideline
        request1 = GenerateGuidelineRequest(
            patient_id=patient.id,
            surgery_name="Cataract Surgery",
            anesthesia_type="local",
            surgery_date=date.today() + timedelta(days=7),
            surgeon_name="Dr. Maria Garcia",
            anesthesiologist_name="Dr. Robert Taylor",
            return_language=None  # Generate all languages
        )
        
        guidelines1 = await anesthesia_service.generate_guideline_multilingual(db, request1)
        print(f"✅ Created {len(guidelines1)} anesthesia guidelines for cataract surgery")
        
        # Create another guideline for a different surgery
        request2 = GenerateGuidelineRequest(
            patient_id=patient.id,
            surgery_name="Gallbladder Removal",
            anesthesia_type="general",
            surgery_date=date.today() + timedelta(days=14),
            surgeon_name="Dr. Michael Chen",
            anesthesiologist_name="Dr. Sarah Johnson",
            return_language=None  # Generate all languages
        )
        
        guidelines2 = await anesthesia_service.generate_guideline_multilingual(db, request2)
        print(f"✅ Created {len(guidelines2)} anesthesia guidelines for gallbladder removal")
        
        db.commit()
        print(f"✅ Total anesthesia guidelines created: {db.query(AnesthesiaGuideline).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating anesthesia guidelines: {e}")
        raise
    finally:
        db.close()

async def main():
    """Main initialization function"""
    print("🚀 Starting Complete Multilingual System Initialization...")
    print("=" * 60)
    
    try:
        # Step 1: Run database migrations
        await run_database_migrations()
        
        # Step 2: Create anesthesia templates
        await create_anesthesia_templates()
        
        # Step 3: Create multilingual sample patients
        await create_multilingual_sample_patients()
        
        # Step 4: Create sample anesthesia guidelines
        await create_sample_anesthesia_guidelines()
        
        print("\n" + "=" * 60)
        print("🎉 Multilingual System Initialization Complete!")
        print("\n📋 System Summary:")
        print("✅ Database migrations completed")
        print("✅ Anesthesia templates created")
        print("✅ Multilingual sample patients created")
        print("✅ Multilingual medical histories created")
        print("✅ Multilingual surgery records created")
        print("✅ Multilingual anesthesia guidelines created")
        print("\n🌐 Supported Languages: English (EN), Chinese (ZH), French (FR)")
        print("\n🔗 API Endpoints Available:")
        print("- GET /api/v1/patients/{id}?language=zh")
        print("- GET /api/v1/patients/{id}/medical-history?language=fr")
        print("- GET /api/v1/patients/{id}/surgery-records?language=zh")
        print("- POST /api/v1/patients/{id}/medical-history (creates all languages)")
        print("- POST /api/v1/patients/{id}/surgery-records (creates all languages)")
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
