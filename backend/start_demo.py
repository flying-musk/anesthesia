#!/usr/bin/env python
"""
Quick start script - for hackathon demo
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db
from app.models.patient import Patient, MedicalHistory, SurgeryRecord
from app.models.anesthesia import AnesthesiaGuidelineTemplate
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from datetime import date


async def create_demo_data():
    """Create demo data"""
    print("Creating demo data...")

    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Patient).count() > 0:
            print("Data already exists, skipping creation")
            return

        # Create patient 1
        patient1 = Patient(
            health_insurance_number='1234567890',
            full_name='John Smith',
            date_of_birth=date(1985, 5, 15),
            gender='M',
            phone_number='555-0123',
            emergency_contact_name='Jane Smith',
            emergency_contact_relationship='Spouse',
            emergency_contact_phone='555-0124'
        )

        db.add(patient1)
        db.commit()
        db.refresh(patient1)

        # Create medical history for patient 1
        medical_history1 = MedicalHistory(
            patient_id=patient1.id,
            allergies='Penicillin allergy',
            chronic_conditions='Hypertension',
            current_medications='Blood pressure medication',
            previous_surgeries='Appendectomy (2010)',
            family_history='Father has diabetes'
        )
        
        db.add(medical_history1)

        # Create patient 2
        patient2 = Patient(
            health_insurance_number='0987654321',
            full_name='Emily Johnson',
            date_of_birth=date(1990, 8, 22),
            gender='F',
            phone_number='555-4321',
            emergency_contact_name='Robert Johnson',
            emergency_contact_relationship='Father',
            emergency_contact_phone='555-4322'
        )

        db.add(patient2)
        db.commit()
        db.refresh(patient2)

        # Create medical history for patient 2
        medical_history2 = MedicalHistory(
            patient_id=patient2.id,
            allergies='None',
            chronic_conditions='None',
            current_medications='None',
            previous_surgeries='None',
            family_history='Mother has breast cancer history'
        )

        db.add(medical_history2)

        # Create anesthesia template
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
        db.commit()

        print("✅ Demo data creation completed!")
        print(f"📊 Created {db.query(Patient).count()} patients")
        print(f"📋 Created {db.query(AnesthesiaGuidelineTemplate).count()} templates")
        print("\n🎯 Demo patient information:")
        print("Patient 1: John Smith (Insurance #: 1234567890)")
        print("Patient 2: Emily Johnson (Insurance #: 0987654321)")
        
    finally:
        db.close()


async def main():
    """Main function"""
    print("🚀 Starting Anesthesia Management System Demo...")
    print("=" * 50)

    # Initialize database
    print("📁 Initializing SQLite database...")
    await init_db()
    print("✅ Database initialization completed")

    # Create demo data
    await create_demo_data()

    print("=" * 50)
    print("🎉 System ready!")
    print("\n📖 Usage instructions:")
    print("1. Start server: uvicorn app.main:app --reload")
    print("2. View API docs: http://localhost:8000/docs")
    print("3. Test API: python scripts/test_api.py")
    print("\n🔍 Demo patient search example:")
    print("Insurance #: 1234567890")
    print("Name: John Smith")
    print("Date of Birth: 1985-05-15")


if __name__ == '__main__':
    asyncio.run(main())
