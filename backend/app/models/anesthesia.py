"""
麻醉須知相關資料庫模型
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class AnesthesiaGuideline(Base):
    """麻醉須知模型"""
    __tablename__ = "anesthesia_guidelines"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    language = Column(String(10), nullable=False, default="en")  # en, zh, fr
    group_id = Column(Integer, nullable=True, index=True)  # 用於關聯同一組的多語言版本

    # 手術和麻醉資訊
    surgery_name = Column(String(200), nullable=False)
    anesthesia_type = Column(String(20), nullable=False)  # general, local, regional, sedation
    surgery_date = Column(Date, nullable=False)
    surgeon_name = Column(String(100), nullable=True)
    anesthesiologist_name = Column(String(100), nullable=True)

    # AI 生成的須知內容
    anesthesia_type_info = Column(Text, nullable=False)
    surgery_process = Column(Text, nullable=False)
    expected_sensations = Column(Text, nullable=False)
    potential_risks = Column(Text, nullable=False)
    pre_surgery_instructions = Column(Text, nullable=False)
    fasting_instructions = Column(Text, nullable=False)
    medication_instructions = Column(Text, nullable=False)
    common_questions = Column(Text, nullable=False)
    post_surgery_care = Column(Text, nullable=False)

    # 其他資訊
    additional_notes = Column(Text, nullable=True)

    # 生成狀態
    is_generated = Column(Boolean, default=False, nullable=False)
    generation_notes = Column(Text, nullable=True)

    # 時間戳記
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 關聯
    patient = relationship("Patient")


class AnesthesiaGuidelineTemplate(Base):
    """麻醉須知模板模型"""
    __tablename__ = "anesthesia_guideline_templates"

    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String(100), nullable=False)
    anesthesia_type = Column(String(20), nullable=False)

    # 模板內容
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

    # 時間戳記
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class GenerationJob(Base):
    """Records an LLM generation or translation job (prompt, model, response, status)."""
    __tablename__ = 'generation_jobs'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=True)
    guideline_id = Column(Integer, ForeignKey('anesthesia_guidelines.id'), nullable=True)
    model = Column(String(200), nullable=True)
    prompt = Column(Text, nullable=True)
    response = Column(Text, nullable=True)
    language = Column(String(10), nullable=True)
    is_translation = Column(Boolean, default=False, nullable=False)
    status = Column(String(50), default='completed', nullable=False)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class GeneratedField(Base):
    """Stores individual generated textual fields (for provenance per field)."""
    __tablename__ = 'generated_fields'

    id = Column(Integer, primary_key=True, index=True)
    guideline_id = Column(Integer, ForeignKey('anesthesia_guidelines.id'), nullable=True)
    field_name = Column(String(100), nullable=False)
    language = Column(String(10), nullable=False)
    content = Column(Text, nullable=True)
    generation_job_id = Column(Integer, ForeignKey('generation_jobs.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    guideline = relationship('AnesthesiaGuideline', backref='generated_fields')
    job = relationship('GenerationJob', backref='generated_fields')


class TranslationRecord(Base):
    """Records translations of arbitrary source texts (medical history, surgery notes, etc.)."""
    __tablename__ = 'translation_records'

    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String(50), nullable=False)  # e.g., 'medical_history', 'surgery_record'
    source_id = Column(Integer, nullable=True)
    field_name = Column(String(100), nullable=True)
    source_text = Column(Text, nullable=True)
    target_language = Column(String(10), nullable=False)
    translated_text = Column(Text, nullable=True)
    generation_job_id = Column(Integer, ForeignKey('generation_jobs.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship('GenerationJob', backref='translation_records')
