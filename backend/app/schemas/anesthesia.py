"""
麻醉須知相關 Pydantic 模型
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Union
from datetime import date, datetime
from enum import Enum


class AnesthesiaTypeEnum(str, Enum):
    """麻醉類型枚舉"""
    GENERAL = "general"
    LOCAL = "local"
    REGIONAL = "regional"
    SEDATION = "sedation"


class AnesthesiaGuidelineBase(BaseModel):
    """麻醉須知基礎模型"""
    surgery_name: str = Field(..., max_length=200, description="手術名稱")
    anesthesia_type: AnesthesiaTypeEnum = Field(..., description="麻醉類型")
    surgery_date: date = Field(..., description="手術日期")
    surgeon_name: Optional[str] = Field(None, max_length=100, description="主刀醫師")
    anesthesiologist_name: Optional[str] = Field(None, max_length=100, description="麻醉醫師")
    
    # AI 生成的須知內容
    anesthesia_type_info: str = Field(..., description="麻醉類型說明")
    surgery_process: str = Field(..., description="手術過程")
    expected_sensations: str = Field(..., description="預期感受")
    potential_risks: str = Field(..., description="可能風險")
    pre_surgery_instructions: str = Field(..., description="術前須知")
    fasting_instructions: str = Field(..., description="禁食禁水須知")
    medication_instructions: str = Field(..., description="藥物停用須知")
    common_questions: str = Field(..., description="常見問題")
    post_surgery_care: str = Field(..., description="術後照護")
    
    # 其他資訊
    additional_notes: Optional[str] = Field(None, description="其他注意事項")


class AnesthesiaGuidelineCreate(BaseModel):
    """建立麻醉須知模型"""
    patient_id: int = Field(..., description="患者 ID")
    surgery_name: str = Field(..., max_length=200, description="手術名稱")
    anesthesia_type: AnesthesiaTypeEnum = Field(..., description="麻醉類型")
    surgery_date: date = Field(..., description="手術日期")
    surgeon_name: Optional[str] = Field(None, max_length=100, description="主刀醫師")
    anesthesiologist_name: Optional[str] = Field(None, max_length=100, description="麻醉醫師")


class AnesthesiaGuidelineUpdate(BaseModel):
    """更新麻醉須知模型"""
    surgery_name: Optional[str] = Field(None, max_length=200)
    anesthesia_type: Optional[AnesthesiaTypeEnum] = None
    surgery_date: Optional[date] = None
    surgeon_name: Optional[str] = Field(None, max_length=100)
    anesthesiologist_name: Optional[str] = Field(None, max_length=100)
    additional_notes: Optional[str] = None


class AnesthesiaGuidelineResponse(AnesthesiaGuidelineBase):
    """麻醉須知回應模型"""
    id: int
    patient_id: int
    is_generated: bool
    generation_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AnesthesiaGuidelineTemplateBase(BaseModel):
    """麻醉須知模板基礎模型"""
    template_name: str = Field(..., max_length=100, description="模板名稱")
    anesthesia_type: AnesthesiaTypeEnum = Field(..., description="麻醉類型")
    
    # 模板內容
    anesthesia_type_template: str = Field(..., description="麻醉類型模板")
    surgery_process_template: str = Field(..., description="手術過程模板")
    expected_sensations_template: str = Field(..., description="預期感受模板")
    potential_risks_template: str = Field(..., description="可能風險模板")
    pre_surgery_template: str = Field(..., description="術前須知模板")
    fasting_template: str = Field(..., description="禁食禁水模板")
    medication_template: str = Field(..., description="藥物停用模板")
    common_questions_template: str = Field(..., description="常見問題模板")
    post_surgery_template: str = Field(..., description="術後照護模板")
    
    is_active: bool = Field(True, description="是否啟用")


class AnesthesiaGuidelineTemplateCreate(AnesthesiaGuidelineTemplateBase):
    """建立麻醉須知模板模型"""
    pass


class AnesthesiaGuidelineTemplateUpdate(BaseModel):
    """更新麻醉須知模板模型"""
    template_name: Optional[str] = Field(None, max_length=100)
    anesthesia_type: Optional[AnesthesiaTypeEnum] = None
    anesthesia_type_template: Optional[str] = None
    surgery_process_template: Optional[str] = None
    expected_sensations_template: Optional[str] = None
    potential_risks_template: Optional[str] = None
    pre_surgery_template: Optional[str] = None
    fasting_template: Optional[str] = None
    medication_template: Optional[str] = None
    common_questions_template: Optional[str] = None
    post_surgery_template: Optional[str] = None
    is_active: Optional[bool] = None


class AnesthesiaGuidelineTemplateResponse(AnesthesiaGuidelineTemplateBase):
    """麻醉須知模板回應模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GenerateGuidelineRequest(BaseModel):
    """生成麻醉須知請求模型"""
    patient_id: int = Field(..., description="患者 ID")
    surgery_name: str = Field(..., max_length=200, description="手術名稱")
    anesthesia_type: AnesthesiaTypeEnum = Field(..., description="麻醉類型")
    surgery_date: Union[date, datetime] = Field(..., description="手術日期")
    surgeon_name: Optional[str] = Field(None, max_length=100, description="主刀醫師")
    anesthesiologist_name: Optional[str] = Field(None, max_length=100, description="麻醉醫師")
    
    @validator('surgery_date')
    def validate_surgery_date(cls, v):
        """驗證並轉換手術日期"""
        if isinstance(v, datetime):
            return v.date()
        return v


class AnesthesiaGuidelineWithPatient(AnesthesiaGuidelineResponse):
    """包含患者資訊的麻醉須知回應模型"""
    patient: Optional[dict] = None
