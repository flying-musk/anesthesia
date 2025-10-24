"""
患者相關資料庫模型
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Patient(Base):
    """患者模型"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    health_insurance_number = Column(String(20), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(1), nullable=False)  # M, F, O
    phone_number = Column(String(15), nullable=True)
    
    # 緊急聯絡人
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_relationship = Column(String(50), nullable=True)
    emergency_contact_phone = Column(String(15), nullable=True)
    
    # 時間戳記
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 關聯
    medical_history = relationship("MedicalHistory", back_populates="patient", uselist=False)
    surgery_records = relationship("SurgeryRecord", back_populates="patient")
    anesthesia_guidelines = relationship("AnesthesiaGuideline", back_populates="patient")


class MedicalHistory(Base):
    """醫療病史模型"""
    __tablename__ = "medical_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # 醫療資訊
    allergies = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    current_medications = Column(Text, nullable=True)
    previous_surgeries = Column(Text, nullable=True)
    family_history = Column(Text, nullable=True)
    other_medical_info = Column(Text, nullable=True)
    
    # 時間戳記
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 關聯
    patient = relationship("Patient", back_populates="medical_history")


class SurgeryRecord(Base):
    """手術記錄模型"""
    __tablename__ = "surgery_records"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # 手術資訊
    surgery_name = Column(String(200), nullable=False)
    surgery_type = Column(String(20), nullable=False)  # general, local, regional, sedation
    surgery_date = Column(Date, nullable=False)
    surgeon_name = Column(String(100), nullable=False)
    anesthesiologist_name = Column(String(100), nullable=False)
    
    # 手術相關資訊
    surgery_duration = Column(Integer, nullable=True)  # 分鐘
    anesthesia_duration = Column(Integer, nullable=True)  # 分鐘
    
    # 術前評估
    pre_surgery_assessment = Column(Text, nullable=True)
    
    # 術後狀況
    post_surgery_notes = Column(Text, nullable=True)
    
    # 併發症
    complications = Column(Text, nullable=True)
    
    # 時間戳記
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 關聯
    patient = relationship("Patient", back_populates="surgery_records")
