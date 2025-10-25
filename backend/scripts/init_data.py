#!/usr/bin/env python
"""
Data Initialization Script - FastAPI Version
For creating test data and default templates
"""

import asyncio
import sys
import os
from datetime import date

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.models.patient import Patient, MedicalHistory, SurgeryRecord
from app.models.anesthesia import AnesthesiaGuidelineTemplate


async def create_sample_patients():
    """Create sample patient data"""
    print("Creating sample patient data...")

    db = SessionLocal()
    try:
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
        db.commit()

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
        db.commit()

        print(f"Created {db.query(Patient).count()} patients")

    finally:
        db.close()


async def create_anesthesia_templates():
    """Create anesthesia guideline templates"""
    print("Creating anesthesia guideline templates...")

    db = SessionLocal()
    try:
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
        db.commit()

        print(f"Created {db.query(AnesthesiaGuidelineTemplate).count()} templates")

    finally:
        db.close()


async def main():
    """Main function"""
    print("Starting data initialization...")

    # Initialize database
    await init_db()

    # Create sample patients
    await create_sample_patients()

    # Create anesthesia templates
    await create_anesthesia_templates()

    print("Data initialization completed!")
    print("\nSample patient information:")
    print("Patient 1: John Smith (Insurance #: 1234567890)")
    print("Patient 2: Emily Johnson (Insurance #: 0987654321)")


if __name__ == '__main__':
    asyncio.run(main())
