#!/usr/bin/env python3
"""
Initialize multilingual sample data for the anesthesia management system
"""

import sys
import os
from datetime import date, datetime, timedelta
import random
import time

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db, engine
from app.models.patient import Patient, MedicalHistory, SurgeryRecord
from app.models.anesthesia import AnesthesiaGuideline
from sqlalchemy.orm import Session

def create_multilingual_sample_data():
    """Create multilingual sample data for patients, medical history and surgery records"""
    
    # Get database session
    db = next(get_db())
    
    print("=== Creating Multilingual Sample Data ===")
    
    # Sample medical conditions in multiple languages
    medical_data = {
        "en": {
            "allergies": [
                "Penicillin allergy",
                "Latex allergy", 
                "Shellfish allergy",
                "Pollen allergy",
                "No known allergies"
            ],
            "chronic_conditions": [
                "Hypertension",
                "Diabetes Type 2",
                "Asthma",
                "Heart disease",
                "Arthritis",
                "None"
            ],
            "medications": [
                "Metformin 500mg daily",
                "Lisinopril 10mg daily",
                "Albuterol inhaler as needed",
                "Aspirin 81mg daily",
                "None"
            ],
            "surgeries": [
                "Appendectomy",
                "Gallbladder removal",
                "Cataract surgery",
                "Colonoscopy",
                "Cardiac catheterization"
            ]
        },
        "zh": {
            "allergies": [
                "青黴素過敏",
                "乳膠過敏",
                "海鮮過敏",
                "花粉過敏",
                "無已知過敏"
            ],
            "chronic_conditions": [
                "高血壓",
                "2型糖尿病",
                "哮喘",
                "心臟病",
                "關節炎",
                "無"
            ],
            "medications": [
                "二甲雙胍500mg每日",
                "賴諾普利10mg每日",
                "沙丁胺醇吸入器按需使用",
                "阿司匹林81mg每日",
                "無"
            ],
            "surgeries": [
                "闌尾切除術",
                "膽囊切除術",
                "白內障手術",
                "結腸鏡檢查",
                "心導管檢查"
            ]
        },
        "fr": {
            "allergies": [
                "Allergie à la pénicilline",
                "Allergie au latex",
                "Allergie aux fruits de mer",
                "Allergie au pollen",
                "Aucune allergie connue"
            ],
            "chronic_conditions": [
                "Hypertension",
                "Diabète de type 2",
                "Asthme",
                "Maladie cardiaque",
                "Arthrite",
                "Aucune"
            ],
            "medications": [
                "Metformine 500mg quotidien",
                "Lisinopril 10mg quotidien",
                "Inhalateur d'albutérol si nécessaire",
                "Aspirine 81mg quotidien",
                "Aucune"
            ],
            "surgeries": [
                "Appendicectomie",
                "Ablation de la vésicule biliaire",
                "Chirurgie de la cataracte",
                "Colonoscopie",
                "Cathétérisme cardiaque"
            ]
        }
    }
    
    # Sample patients
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
            "health_insurance_number": "1234567891",
            "full_name": "Test Patient",
            "date_of_birth": date(1990, 1, 1),
            "gender": "M",
        }
    ]
    
    # Create patients
    patient_objects = []
    for p_data in patients_data:
        patient = db.query(Patient).filter(
            Patient.health_insurance_number == p_data["health_insurance_number"]
        ).first()
        if not patient:
            patient = Patient(**p_data)
            db.add(patient)
            db.commit()
            db.refresh(patient)
            print(f"Created patient: {patient.full_name}")
        else:
            print(f"Patient already exists: {patient.full_name}")
        patient_objects.append(patient)
    
    # Create multilingual medical histories
    for patient in patient_objects:
        print(f"\n--- Creating multilingual medical history for {patient.full_name} ---")
        
        # Check if medical history already exists
        existing_history = db.query(MedicalHistory).filter(
            MedicalHistory.patient_id == patient.id
        ).first()
        
        if not existing_history:
            # Generate group_id
            group_id = int(time.time() * 1000)
            
            # Create medical history in all three languages
            for lang_code, lang_data in medical_data.items():
                medical_history = MedicalHistory(
                    patient_id=patient.id,
                    language=lang_code,
                    group_id=group_id,
                    allergies=random.choice(lang_data["allergies"]),
                    chronic_conditions=random.choice(lang_data["chronic_conditions"]),
                    current_medications=random.choice(lang_data["medications"]),
                    previous_surgeries=random.choice(lang_data["surgeries"]),
                    family_history=f"Family history of {random.choice(['heart disease', 'diabetes', 'cancer', 'none'])}" if lang_code == "en" else f"家族病史：{random.choice(['心臟病', '糖尿病', '癌症', '無'])}" if lang_code == "zh" else f"Antécédents familiaux: {random.choice(['maladie cardiaque', 'diabète', 'cancer', 'aucun'])}",
                    other_medical_info=f"Patient has been stable with current medications. Last checkup: {date.today()}" if lang_code == "en" else f"患者目前用藥穩定。最後檢查：{date.today()}" if lang_code == "zh" else f"Le patient est stable avec ses médicaments actuels. Dernier contrôle: {date.today()}"
                )
                db.add(medical_history)
                print(f"✓ Created medical history in {lang_code.upper()}")
            
            db.commit()
        else:
            print(f"✓ Medical history already exists for {patient.full_name}")
    
    # Create multilingual surgery records
    surgery_types = ["general", "local", "regional", "sedation"]
    surgeons = ["Dr. Michael Chen", "Dr. Sarah Johnson", "Dr. Lisa Wang", "Dr. Robert Taylor", "Dr. Maria Garcia"]
    anesthesiologists = ["Dr. Robert Taylor", "Dr. Maria Garcia", "Dr. Christopher Brown"]
    
    for patient in patient_objects:
        print(f"\n--- Creating multilingual surgery records for {patient.full_name} ---")
        
        # Create 2-3 surgery records per patient
        num_records = random.randint(2, 3)
        for i in range(num_records):
            # Generate group_id for this surgery
            group_id = int(time.time() * 1000) + i
            
            # Create surgery record in all three languages
            for lang_code, lang_data in medical_data.items():
                surgery_name = random.choice(lang_data["surgeries"])
                surgery_type = random.choice(surgery_types)
                surgery_date = date.today() - timedelta(days=random.randint(30, 365))
                
                # Create multilingual surgery record
                surgery_record = SurgeryRecord(
                    patient_id=patient.id,
                    language=lang_code,
                    group_id=group_id,
                    surgery_name=surgery_name,
                    surgery_type=surgery_type,
                    surgery_date=surgery_date,
                    surgeon_name=random.choice(surgeons),
                    anesthesiologist_name=random.choice(anesthesiologists),
                    surgery_duration=random.randint(60, 180),
                    anesthesia_duration=random.randint(30, 120),
                    pre_surgery_assessment=f"Patient assessed for {surgery_name}. Vital signs stable. No contraindications for {surgery_type} anesthesia." if lang_code == "en" else f"患者評估 {surgery_name}。生命體徵穩定。無 {surgery_type} 麻醉禁忌症。" if lang_code == "zh" else f"Patient évalué pour {surgery_name}. Signes vitaux stables. Aucune contre-indication pour l'anesthésie {surgery_type}.",
                    post_surgery_notes=f"Patient recovered well from {surgery_name}. No complications noted. Discharged same day." if lang_code == "en" else f"患者從 {surgery_name} 恢復良好。無併發症。當日出院。" if lang_code == "zh" else f"Le patient s'est bien remis de {surgery_name}. Aucune complication notée. Sorti le même jour.",
                    complications="None" if lang_code == "en" else "無" if lang_code == "zh" else "Aucune"
                )
                db.add(surgery_record)
            
            print(f"✓ Created surgery record {i+1} in all languages")
        
        db.commit()
    
    print("\n=== Multilingual Sample Data Creation Complete ===")
    
    # Verify data
    total_patients = db.query(Patient).count()
    total_medical_histories = db.query(MedicalHistory).count()
    total_surgery_records = db.query(SurgeryRecord).count()
    
    print(f"\n=== Data Summary ===")
    print(f"Total patients: {total_patients}")
    print(f"Total medical histories: {total_medical_histories}")
    print(f"Total surgery records: {total_surgery_records}")
    
    # Show language distribution
    print(f"\n=== Language Distribution ===")
    for lang in ["en", "zh", "fr"]:
        mh_count = db.query(MedicalHistory).filter(MedicalHistory.language == lang).count()
        sr_count = db.query(SurgeryRecord).filter(SurgeryRecord.language == lang).count()
        print(f"{lang.upper()}: {mh_count} medical histories, {sr_count} surgery records")
    
    db.close()

if __name__ == "__main__":
    create_multilingual_sample_data()
