"""
Pydantic models for patients.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Generic, TypeVar
from datetime import date, datetime
from enum import Enum
from math import ceil

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int


class GenderEnum(str, Enum):
    """Gender enumeration."""
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class PatientBase(BaseModel):
    """Base model for a patient."""
    health_insurance_number: str = Field(..., min_length=10, max_length=10, description="Health Insurance Number")
    full_name: str = Field(..., min_length=1, max_length=100, description="Full Name")
    date_of_birth: date = Field(..., description="Date of Birth")
    gender: GenderEnum = Field(..., description="Gender")
    phone_number: Optional[str] = Field(None, max_length=15, description="Phone Number")
    emergency_contact_name: Optional[str] = Field(None, max_length=100, description="Emergency Contact Name")
    emergency_contact_relationship: Optional[str] = Field(None, max_length=50, description="Relationship")
    emergency_contact_phone: Optional[str] = Field(None, max_length=15, description="Emergency Contact Phone")
    
    @validator('health_insurance_number')
    def validate_health_insurance_number(cls, v):
        if not v.isdigit():
            raise ValueError('Health insurance number must be numeric')
        return v


class PatientCreate(PatientBase):
    """Model for creating a patient."""
    pass


class PatientUpdate(BaseModel):
    """Model for updating a patient."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=15)
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_relationship: Optional[str] = Field(None, max_length=50)
    emergency_contact_phone: Optional[str] = Field(None, max_length=15)


class PatientResponse(PatientBase):
    """Response model for a patient."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MedicalHistoryBase(BaseModel):
    """Base model for medical history."""
    allergies: Optional[str] = Field(None, description="Allergies")
    chronic_conditions: Optional[str] = Field(None, description="Chronic Conditions")
    current_medications: Optional[str] = Field(None, description="Current Medications")
    previous_surgeries: Optional[str] = Field(None, description="Previous Surgeries")
    family_history: Optional[str] = Field(None, description="Family History")
    other_medical_info: Optional[str] = Field(None, description="Other Medical Information")


class MedicalHistoryCreate(MedicalHistoryBase):
    """Model for creating medical history."""
    patient_id: int


class MedicalHistoryUpdate(MedicalHistoryBase):
    """Model for updating medical history."""
    pass


class MedicalHistoryResponse(MedicalHistoryBase):
    """Response model for medical history."""
    id: int
    patient_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SurgeryRecordBase(BaseModel):
    """Base model for a surgery record."""
    surgery_name: str = Field(..., max_length=200, description="Surgery Name")
    surgery_type: str = Field(..., max_length=20, description="Anesthesia Type")
    surgery_date: date = Field(..., description="Surgery Date")
    surgeon_name: str = Field(..., max_length=100, description="Surgeon Name")
    anesthesiologist_name: str = Field(..., max_length=100, description="Anesthesiologist Name")
    surgery_duration: Optional[int] = Field(None, description="Surgery Duration (minutes)")
    anesthesia_duration: Optional[int] = Field(None, description="Anesthesia Duration (minutes)")
    pre_surgery_assessment: Optional[str] = Field(None, description="Pre-Surgery Assessment")
    post_surgery_notes: Optional[str] = Field(None, description="Post-Surgery Notes")
    complications: Optional[str] = Field(None, description="Complications")


class SurgeryRecordCreate(SurgeryRecordBase):
    """Model for creating a surgery record."""
    patient_id: int


class SurgeryRecordUpdate(BaseModel):
    """Model for updating a surgery record."""
    surgery_name: Optional[str] = Field(None, max_length=200)
    surgery_type: Optional[str] = Field(None, max_length=20)
    surgery_date: Optional[date] = None
    surgeon_name: Optional[str] = Field(None, max_length=100)
    anesthesiologist_name: Optional[str] = Field(None, max_length=100)
    surgery_duration: Optional[int] = None
    anesthesia_duration: Optional[int] = None
    pre_surgery_assessment: Optional[str] = None
    post_surgery_notes: Optional[str] = None
    complications: Optional[str] = None


class SurgeryRecordResponse(SurgeryRecordBase):
    """Response model for a surgery record."""
    id: int
    patient_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PatientSearchRequest(BaseModel):
    """Request model for searching a patient."""
    health_insurance_number: str = Field(..., min_length=10, max_length=10)
    full_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    
    @validator('health_insurance_number')
    def validate_health_insurance_number(cls, v):
        if not v.isdigit():
            raise ValueError('Health insurance number must be numeric')
        return v


class PatientDetailResponse(PatientResponse):
    """Detailed response model for a patient, including medical history and surgery records."""
    medical_history: Optional[MedicalHistoryResponse] = None
    surgery_records: List[SurgeryRecordResponse] = []
