"""
患者相關 API 端點
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.patient import Patient, MedicalHistory, SurgeryRecord
from app.schemas.patient import (
    PatientCreate, PatientUpdate, PatientResponse, PatientDetailResponse,
    PatientSearchRequest, MedicalHistoryCreate, MedicalHistoryUpdate,
    MedicalHistoryResponse, SurgeryRecordCreate, SurgeryRecordUpdate,
    SurgeryRecordResponse
)

router = APIRouter()


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """建立新患者"""
    # 檢查健保號是否已存在
    existing_patient = db.query(Patient).filter(
        Patient.health_insurance_number == patient.health_insurance_number
    ).first()
    
    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="健保號已存在"
        )
    
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    return db_patient


@router.get("/", response_model=List[PatientResponse])
async def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """獲取所有患者"""
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients


@router.get("/{patient_id}", response_model=PatientDetailResponse)
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """獲取特定患者詳細資訊"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    # 獲取醫療病史
    medical_history = db.query(MedicalHistory).filter(
        MedicalHistory.patient_id == patient_id
    ).first()
    
    # 獲取手術記錄
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
    """更新患者資訊"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    update_data = patient_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)
    
    db.commit()
    db.refresh(patient)
    
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """刪除患者"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    db.delete(patient)
    db.commit()


@router.post("/search", response_model=PatientDetailResponse)
async def search_patient(search_request: PatientSearchRequest, db: Session = Depends(get_db)):
    """搜尋患者"""
    patient = db.query(Patient).filter(
        Patient.health_insurance_number == search_request.health_insurance_number,
        Patient.full_name == search_request.full_name,
        Patient.date_of_birth == search_request.date_of_birth
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到符合條件的患者"
        )
    
    # 獲取醫療病史
    medical_history = db.query(MedicalHistory).filter(
        MedicalHistory.patient_id == patient.id
    ).first()
    
    # 獲取手術記錄
    surgery_records = db.query(SurgeryRecord).filter(
        SurgeryRecord.patient_id == patient.id
    ).all()
    
    return PatientDetailResponse(
        **patient.__dict__,
        medical_history=medical_history,
        surgery_records=surgery_records
    )


@router.get("/{patient_id}/medical-history", response_model=MedicalHistoryResponse)
async def get_patient_medical_history(patient_id: int, db: Session = Depends(get_db)):
    """獲取患者醫療病史"""
    medical_history = db.query(MedicalHistory).filter(
        MedicalHistory.patient_id == patient_id
    ).first()
    
    if not medical_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="該患者尚未建立醫療病史"
        )
    
    return medical_history


@router.post("/{patient_id}/medical-history", response_model=MedicalHistoryResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_medical_history(
    patient_id: int, 
    medical_history: MedicalHistoryCreate, 
    db: Session = Depends(get_db)
):
    """建立患者醫療病史"""
    # 檢查患者是否存在
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    # 檢查是否已有醫療病史
    existing_history = db.query(MedicalHistory).filter(
        MedicalHistory.patient_id == patient_id
    ).first()
    
    if existing_history:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="該患者已有醫療病史，請使用更新端點"
        )
    
    db_medical_history = MedicalHistory(**medical_history.dict())
    db.add(db_medical_history)
    db.commit()
    db.refresh(db_medical_history)
    
    return db_medical_history


@router.put("/{patient_id}/medical-history", response_model=MedicalHistoryResponse)
async def update_patient_medical_history(
    patient_id: int, 
    medical_history_update: MedicalHistoryUpdate, 
    db: Session = Depends(get_db)
):
    """更新患者醫療病史"""
    medical_history = db.query(MedicalHistory).filter(
        MedicalHistory.patient_id == patient_id
    ).first()
    
    if not medical_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="該患者尚未建立醫療病史"
        )
    
    update_data = medical_history_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(medical_history, field, value)
    
    db.commit()
    db.refresh(medical_history)
    
    return medical_history


@router.get("/{patient_id}/surgery-records", response_model=List[SurgeryRecordResponse])
async def get_patient_surgery_records(patient_id: int, db: Session = Depends(get_db)):
    """獲取患者手術記錄"""
    surgery_records = db.query(SurgeryRecord).filter(
        SurgeryRecord.patient_id == patient_id
    ).all()
    
    return surgery_records


@router.post("/{patient_id}/surgery-records", response_model=SurgeryRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_surgery_record(
    patient_id: int, 
    surgery_record: SurgeryRecordCreate, 
    db: Session = Depends(get_db)
):
    """建立患者手術記錄"""
    # 檢查患者是否存在
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    db_surgery_record = SurgeryRecord(**surgery_record.dict())
    db.add(db_surgery_record)
    db.commit()
    db.refresh(db_surgery_record)
    
    return db_surgery_record
