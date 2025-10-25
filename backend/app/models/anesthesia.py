"""
Anesthesia guideline-related database models
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class AnesthesiaGuideline(Base):
    """Anesthesia guideline model"""
    __tablename__ = "anesthesia_guidelines"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    language = Column(String(10), nullable=False, default="en")  # en, zh, fr
    group_id = Column(Integer, nullable=True, index=True)  # 用於關聯同一組的多語言版本
    
    # Surgery and anesthesia information
    surgery_name = Column(String(200), nullable=False)
    anesthesia_type = Column(String(20), nullable=False)  # general, local, regional, sedation
    surgery_date = Column(Date, nullable=False)
    surgeon_name = Column(String(100), nullable=True)
    anesthesiologist_name = Column(String(100), nullable=True)

    # AI-generated guideline content
    anesthesia_type_info = Column(Text, nullable=False)
    surgery_process = Column(Text, nullable=False)
    expected_sensations = Column(Text, nullable=False)
    potential_risks = Column(Text, nullable=False)
    pre_surgery_instructions = Column(Text, nullable=False)
    fasting_instructions = Column(Text, nullable=False)
    medication_instructions = Column(Text, nullable=False)
    common_questions = Column(Text, nullable=False)
    post_surgery_care = Column(Text, nullable=False)

    # Other information
    additional_notes = Column(Text, nullable=True)

    # Generation status
    is_generated = Column(Boolean, default=False, nullable=False)
    generation_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
<<<<<<< HEAD
    
    # 關聯
    patient = relationship("Patient")
=======

    # Relationships
    patient = relationship("Patient", back_populates="anesthesia_guidelines")
>>>>>>> Troy


class AnesthesiaGuidelineTemplate(Base):
    """Anesthesia guideline template model"""
    __tablename__ = "anesthesia_guideline_templates"

    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String(100), nullable=False)
    anesthesia_type = Column(String(20), nullable=False)

    # Template content
    anesthesia_type_template = Column(Text, nullable=False)
    surgery_process_template = Column(Text, nullable=False)
    expected_sensations_template = Column(Text, nullable=False)
    potential_risks_template = Column(Text, nullable=False)
    pre_surgery_template = Column(Text, nullable=False)
    fasting_template = Column(Text, nullable=False)
    medication_template = Column(Text, nullable=False)
    common_questions_template = Column(Text, nullable=False)
    post_surgery_template = Column(Text, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
