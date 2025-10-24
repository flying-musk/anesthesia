"""
患者相關 Pydantic 模型
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class GenderEnum(str, Enum):
    """性別枚舉"""
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class PatientBase(BaseModel):
    """患者基礎模型"""
    health_insurance_number: str = Field(..., min_length=10, max_length=10, description="健保號")
    full_name: str = Field(..., min_length=1, max_length=100, description="全名")
    date_of_birth: date = Field(..., description="生日")
    gender: GenderEnum = Field(..., description="性別")
    phone_number: Optional[str] = Field(None, max_length=15, description="電話號碼")
    emergency_contact_name: Optional[str] = Field(None, max_length=100, description="緊急聯絡人姓名")
    emergency_contact_relationship: Optional[str] = Field(None, max_length=50, description="關係")
    emergency_contact_phone: Optional[str] = Field(None, max_length=15, description="緊急聯絡人電話")
    
    @validator('health_insurance_number')
    def validate_health_insurance_number(cls, v):
        if not v.isdigit():
            raise ValueError('健保號必須是數字')
        return v


class PatientCreate(PatientBase):
    """建立患者模型"""
    pass


class PatientUpdate(BaseModel):
    """更新患者模型"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=15)
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_relationship: Optional[str] = Field(None, max_length=50)
    emergency_contact_phone: Optional[str] = Field(None, max_length=15)


class PatientResponse(PatientBase):
    """患者回應模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MedicalHistoryBase(BaseModel):
    """醫療病史基礎模型"""
    allergies: Optional[str] = Field(None, description="過敏史")
    chronic_conditions: Optional[str] = Field(None, description="慢性疾病")
    current_medications: Optional[str] = Field(None, description="目前用藥")
    previous_surgeries: Optional[str] = Field(None, description="手術史")
    family_history: Optional[str] = Field(None, description="家族病史")
    other_medical_info: Optional[str] = Field(None, description="其他醫療資訊")


class MedicalHistoryCreate(MedicalHistoryBase):
    """建立醫療病史模型"""
    patient_id: int


class MedicalHistoryUpdate(MedicalHistoryBase):
    """更新醫療病史模型"""
    pass


class MedicalHistoryResponse(MedicalHistoryBase):
    """醫療病史回應模型"""
    id: int
    patient_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SurgeryRecordBase(BaseModel):
    """手術記錄基礎模型"""
    surgery_name: str = Field(..., max_length=200, description="手術名稱")
    surgery_type: str = Field(..., max_length=20, description="麻醉類型")
    surgery_date: date = Field(..., description="手術日期")
    surgeon_name: str = Field(..., max_length=100, description="主刀醫師")
    anesthesiologist_name: str = Field(..., max_length=100, description="麻醉醫師")
    surgery_duration: Optional[int] = Field(None, description="手術時間（分鐘）")
    anesthesia_duration: Optional[int] = Field(None, description="麻醉時間（分鐘）")
    pre_surgery_assessment: Optional[str] = Field(None, description="術前評估")
    post_surgery_notes: Optional[str] = Field(None, description="術後記錄")
    complications: Optional[str] = Field(None, description="併發症")


class SurgeryRecordCreate(SurgeryRecordBase):
    """建立手術記錄模型"""
    patient_id: int


class SurgeryRecordUpdate(BaseModel):
    """更新手術記錄模型"""
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
    """手術記錄回應模型"""
    id: int
    patient_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PatientSearchRequest(BaseModel):
    """患者搜尋請求模型"""
    health_insurance_number: str = Field(..., min_length=10, max_length=10)
    full_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    
    @validator('health_insurance_number')
    def validate_health_insurance_number(cls, v):
        if not v.isdigit():
            raise ValueError('健保號必須是數字')
        return v


class PatientDetailResponse(PatientResponse):
    """患者詳細回應模型（包含醫療病史和手術記錄）"""
    medical_history: Optional[MedicalHistoryResponse] = None
    surgery_records: List[SurgeryRecordResponse] = []
