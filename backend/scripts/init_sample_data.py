#!/usr/bin/env python3
"""
Initialize sample data for the anesthesia management system
"""

import sys
import os
from datetime import date, datetime, timedelta
import random

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db, engine
from app.models.patient import Patient, MedicalHistory, SurgeryRecord
from app.models.anesthesia import AnesthesiaGuideline
from sqlalchemy.orm import Session

def create_sample_patients():
    """Create sample patients with medical history and surgery records"""
    
    # Get database session
    db = next(get_db())
    
    print("=== Creating Sample Data ===")
    
    # Sample medical conditions
    allergies = [
        "Penicillin allergy",
        "Latex allergy", 
        "Shellfish allergy",
        "Pollen allergy",
        "No known allergies"
    ]
    
    chronic_conditions = [
        "Hypertension",
        "Diabetes Type 2",
        "Asthma",
        "Heart disease",
        "Arthritis",
        "None"
    ]
    
    medications = [
        "Metformin 500mg daily",
        "Lisinopril 10mg daily",
        "Albuterol inhaler as needed",
        "Aspirin 81mg daily",
        "None"
    ]
    
    surgery_types = ["general", "local", "regional", "sedation"]
    surgery_names = [
        "Appendectomy",
        "Gallbladder removal",
        "Hernia repair",
        "Knee arthroscopy",
        "Cataract surgery",
        "Colonoscopy",
        "Endoscopy",
        "Cardiac catheterization"
    ]
    
    surgeons = [
        "Dr. Sarah Johnson",
        "Dr. Michael Chen", 
        "Dr. Emily Rodriguez",
        "Dr. David Kim",
        "Dr. Lisa Wang"
    ]
    
    anesthesiologists = [
        "Dr. James Wilson",
        "Dr. Maria Garcia",
        "Dr. Robert Taylor",
        "Dr. Jennifer Lee",
        "Dr. Christopher Brown"
    ]
    
    # Get existing patients
    patients = db.query(Patient).all()
    print(f"Found {len(patients)} existing patients")
    
    for i, patient in enumerate(patients):
        print(f"\n--- Processing Patient {patient.id}: {patient.full_name} ---")
        
        # Create medical history if it doesn't exist
        existing_history = db.query(MedicalHistory).filter(
            MedicalHistory.patient_id == patient.id
        ).first()
        
        if not existing_history:
            medical_history = MedicalHistory(
                patient_id=patient.id,
                allergies=random.choice(allergies),
                chronic_conditions=random.choice(chronic_conditions),
                current_medications=random.choice(medications),
                previous_surgeries=f"Previous {random.choice(surgery_names)} in {random.randint(2015, 2023)}" if random.random() > 0.3 else "None",
                family_history=f"Family history of {random.choice(['heart disease', 'diabetes', 'cancer', 'none'])}",
                other_medical_info=f"Patient has been stable with current medications. Last checkup: {datetime.now().strftime('%Y-%m-%d')}"
            )
            db.add(medical_history)
            print(f"✓ Created medical history for {patient.full_name}")
        else:
            print(f"✓ Medical history already exists for {patient.full_name}")
        
        # Create surgery records (1-3 records per patient)
        existing_surgeries = db.query(SurgeryRecord).filter(
            SurgeryRecord.patient_id == patient.id
        ).all()
        
        if not existing_surgeries:
            num_surgeries = random.randint(1, 3)
            for j in range(num_surgeries):
                surgery_date = date.today() - timedelta(days=random.randint(30, 365))
                surgery_name = random.choice(surgery_names)
                surgery_type = random.choice(surgery_types)
                
                surgery_record = SurgeryRecord(
                    patient_id=patient.id,
                    surgery_name=surgery_name,
                    surgery_type=surgery_type,
                    surgery_date=surgery_date,
                    surgeon_name=random.choice(surgeons),
                    anesthesiologist_name=random.choice(anesthesiologists),
                    surgery_duration=random.randint(30, 180),
                    anesthesia_duration=random.randint(15, 120),
                    pre_surgery_assessment=f"Patient assessed for {surgery_name}. Vital signs stable. No contraindications for {surgery_type} anesthesia.",
                    post_surgery_notes=f"Patient recovered well from {surgery_name}. No complications noted. Discharged same day.",
                    complications="None" if random.random() > 0.1 else "Minor nausea post-surgery, resolved with medication"
                )
                db.add(surgery_record)
                print(f"✓ Created surgery record: {surgery_name} ({surgery_type})")
        else:
            print(f"✓ Surgery records already exist for {patient.full_name} ({len(existing_surgeries)} records)")
    
    # Commit all changes
    try:
        db.commit()
        print(f"\n=== Sample Data Creation Complete ===")
        print("✓ All medical histories and surgery records created successfully")
        
        # Verify the data
        total_patients = db.query(Patient).count()
        total_histories = db.query(MedicalHistory).count()
        total_surgeries = db.query(SurgeryRecord).count()
        
        print(f"\n=== Data Summary ===")
        print(f"Total patients: {total_patients}")
        print(f"Total medical histories: {total_histories}")
        print(f"Total surgery records: {total_surgeries}")
        
        # Show some examples
        print(f"\n=== Sample Data Preview ===")
        for patient in patients[:2]:  # Show first 2 patients
            print(f"\nPatient: {patient.full_name}")
            
            history = db.query(MedicalHistory).filter(
                MedicalHistory.patient_id == patient.id
            ).first()
            if history:
                print(f"  Medical History: {history.chronic_conditions}, Allergies: {history.allergies}")
            
            surgeries = db.query(SurgeryRecord).filter(
                SurgeryRecord.patient_id == patient.id
            ).all()
            print(f"  Surgery Records: {len(surgeries)}")
            for surgery in surgeries:
                print(f"    - {surgery.surgery_name} ({surgery.surgery_type}) on {surgery.surgery_date}")
        
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")
        db.rollback()
        raise

if __name__ == "__main__":
    create_sample_patients()
