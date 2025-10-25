"""
Patient-related API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.patient import Patient, MedicalHistory, SurgeryRecord
from app.schemas.patient import (
    PatientCreate, PatientUpdate, PatientResponse, PatientDetailResponse,
    PatientSearchRequest, MedicalHistoryCreate, MedicalHistoryUpdate,
    MedicalHistoryResponse, SurgeryRecordCreate, SurgeryRecordUpdate,
    SurgeryRecordResponse, PaginatedResponse, LanguageEnum
)
from app.services.medical_multilingual_service import medical_multilingual_service
from math import ceil

router = APIRouter()


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient"""
    # Check if health insurance number already exists
    existing_patient = db.query(Patient).filter(
        Patient.health_insurance_number == patient.health_insurance_number
    ).first()

    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Health insurance number already exists"
        )
    
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    return db_patient


@router.get("/", response_model=PaginatedResponse[PatientResponse])
async def get_patients(page: int = 1, size: int = 100, db: Session = Depends(get_db)):
    """Get all patients with pagination"""
    # Calculate offset
    skip = (page - 1) * size

    # Get total count
    total = db.query(Patient).count()

    # Get patients for current page
    patients = db.query(Patient).offset(skip).limit(size).all()

    # Calculate total pages
    pages = ceil(total / size) if size > 0 else 0

    return PaginatedResponse(
        items=patients,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{patient_id}", response_model=PatientDetailResponse)
async def get_patient(
    patient_id: int, 
    language: Optional[LanguageEnum] = Query(None, description="Language preference"),
    db: Session = Depends(get_db)
):
    """Get specific patient details"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Get medical history based on language preference
    if language:
        medical_history = db.query(MedicalHistory).filter(
            MedicalHistory.patient_id == patient_id,
            MedicalHistory.language == language.value
        ).order_by(MedicalHistory.created_at.desc()).first()
    else:
        # Return the most recent medical history if no language specified
        medical_history = db.query(MedicalHistory).filter(
            MedicalHistory.patient_id == patient_id
        ).order_by(MedicalHistory.created_at.desc()).first()

    # Get surgery records based on language preference
    if language:
        surgery_records = db.query(SurgeryRecord).filter(
            SurgeryRecord.patient_id == patient_id,
            SurgeryRecord.language == language.value
        ).all()
    else:
        # Return all surgery records if no language specified
        surgery_records = db.query(SurgeryRecord).filter(
            SurgeryRecord.patient_id == patient_id
        ).all()
    
    return PatientDetailResponse(
        **patient.__dict__,
        medical_history=medical_history,
        surgery_records=surgery_records
    )


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db)
):
    """Update patient information"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    update_data = patient_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)
    
    db.commit()
    db.refresh(patient)
    
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Delete patient"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    db.delete(patient)
    db.commit()


@router.post("/search", response_model=PatientDetailResponse)
async def search_patient(search_request: PatientSearchRequest, db: Session = Depends(get_db)):
    """Search for patient"""
    patient = db.query(Patient).filter(
        Patient.health_insurance_number == search_request.health_insurance_number,
        Patient.full_name == search_request.full_name,
        Patient.date_of_birth == search_request.date_of_birth
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No patient found matching the criteria"
        )

    # Get medical history
    medical_history = db.query(MedicalHistory).filter(
        MedicalHistory.patient_id == patient.id
    ).first()

    # Get surgery records
    surgery_records = db.query(SurgeryRecord).filter(
        SurgeryRecord.patient_id == patient.id
    ).all()
    
    return PatientDetailResponse(
        **patient.__dict__,
        medical_history=medical_history,
        surgery_records=surgery_records
    )


@router.get("/{patient_id}/medical-history", response_model=MedicalHistoryResponse)
async def get_patient_medical_history(
    patient_id: int, 
    language: Optional[LanguageEnum] = Query(None, description="Language preference"),
    db: Session = Depends(get_db)
):
    """Get patient medical history"""
    # If language is specified, find the medical history with the specified language
    if language:
        medical_history = db.query(MedicalHistory).filter(
            MedicalHistory.patient_id == patient_id,
            MedicalHistory.language == language.value
        ).order_by(MedicalHistory.created_at.desc()).first()

        if not medical_history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medical history not found in language: {language.value}"
            )
    else:
        # Return the most recent medical history if no language specified
        medical_history = db.query(MedicalHistory).filter(
            MedicalHistory.patient_id == patient_id
        ).order_by(MedicalHistory.created_at.desc()).first()

        if not medical_history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical history not found for this patient"
            )
    
    return medical_history


@router.post("/{patient_id}/medical-history", response_model=List[MedicalHistoryResponse], status_code=status.HTTP_201_CREATED)
async def create_patient_medical_history(
    patient_id: int,
    medical_history: MedicalHistoryCreate,
    db: Session = Depends(get_db)
):
    """Create patient medical history in multiple languages"""
    # Check if patient exists
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Check if medical history already exists
    existing_history = db.query(MedicalHistory).filter(
        MedicalHistory.patient_id == patient_id
    ).first()

    if existing_history:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medical history already exists for this patient. Please use the update endpoint"
        )
    
    # Create multilingual medical history
    medical_histories = await medical_multilingual_service.create_medical_history_multilingual(
        db, patient_id, medical_history
    )
    
    return medical_histories


@router.put("/{patient_id}/medical-history", response_model=MedicalHistoryResponse)
async def update_patient_medical_history(
    patient_id: int,
    medical_history_update: MedicalHistoryUpdate,
    db: Session = Depends(get_db)
):
    """Update patient medical history"""
    medical_history = db.query(MedicalHistory).filter(
        MedicalHistory.patient_id == patient_id
    ).first()

    if not medical_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical history not found for this patient"
        )
    
    update_data = medical_history_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(medical_history, field, value)
    
    db.commit()
    db.refresh(medical_history)
    
    return medical_history


@router.get("/{patient_id}/surgery-records", response_model=List[SurgeryRecordResponse])
async def get_patient_surgery_records(
    patient_id: int, 
    language: Optional[LanguageEnum] = Query(None, description="Language preference"),
    db: Session = Depends(get_db)
):
    """Get patient surgery records"""
    if language:
        # Get surgery records in the specified language
        surgery_records = db.query(SurgeryRecord).filter(
            SurgeryRecord.patient_id == patient_id,
            SurgeryRecord.language == language.value
        ).all()
    else:
        # Return all surgery records (default behavior)
        surgery_records = db.query(SurgeryRecord).filter(
            SurgeryRecord.patient_id == patient_id
        ).all()

    return surgery_records


@router.post("/{patient_id}/surgery-records", response_model=List[SurgeryRecordResponse], status_code=status.HTTP_201_CREATED)
async def create_patient_surgery_record(
    patient_id: int,
    surgery_record: SurgeryRecordCreate,
    db: Session = Depends(get_db)
):
    """Create patient surgery record in multiple languages"""
    # Check if patient exists
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Create multilingual surgery record
    surgery_records = await medical_multilingual_service.create_surgery_record_multilingual(
        db, patient_id, surgery_record
    )
    
    return surgery_records
