"""
Patient-related database models
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Patient(Base):
    """Patient model"""
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    health_insurance_number = Column(String(20), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(1), nullable=False)  # M, F, O
    phone_number = Column(String(15), nullable=True)

    # Emergency contact
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_relationship = Column(String(50), nullable=True)
    emergency_contact_phone = Column(String(15), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    medical_history = relationship("MedicalHistory", back_populates="patient", uselist=False)
    surgery_records = relationship("SurgeryRecord", back_populates="patient")
    anesthesia_guidelines = relationship("AnesthesiaGuideline", back_populates="patient")


class MedicalHistory(Base):
    """Medical history model"""
    __tablename__ = "medical_histories"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    # Medical information
    allergies = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    current_medications = Column(Text, nullable=True)
    previous_surgeries = Column(Text, nullable=True)
    family_history = Column(Text, nullable=True)
    other_medical_info = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="medical_history")


class SurgeryRecord(Base):
    """Surgery record model"""
    __tablename__ = "surgery_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    # Surgery information
    surgery_name = Column(String(200), nullable=False)
    surgery_type = Column(String(20), nullable=False)  # general, local, regional, sedation
    surgery_date = Column(Date, nullable=False)
    surgeon_name = Column(String(100), nullable=False)
    anesthesiologist_name = Column(String(100), nullable=False)

    # Surgery-related information
    surgery_duration = Column(Integer, nullable=True)  # minutes
    anesthesia_duration = Column(Integer, nullable=True)  # minutes

    # Pre-surgery assessment
    pre_surgery_assessment = Column(Text, nullable=True)

    # Post-surgery status
    post_surgery_notes = Column(Text, nullable=True)

    # Complications
    complications = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="surgery_records")
