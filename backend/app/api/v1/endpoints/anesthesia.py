"""
麻醉須知相關 API 端點
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.models.anesthesia import AnesthesiaGuideline, AnesthesiaGuidelineTemplate
from app.models.patient import Patient
from app.schemas.anesthesia import (
    AnesthesiaGuidelineCreate, AnesthesiaGuidelineUpdate, AnesthesiaGuidelineResponse,
    AnesthesiaGuidelineTemplateCreate, AnesthesiaGuidelineTemplateUpdate,
    AnesthesiaGuidelineTemplateResponse, GenerateGuidelineRequest,
    AnesthesiaGuidelineWithPatient
)
from app.services.anesthesia_service import AnesthesiaGuidelineService

router = APIRouter()


@router.post("/guidelines/generate", response_model=AnesthesiaGuidelineResponse, status_code=status.HTTP_201_CREATED)
async def generate_guideline(request: GenerateGuidelineRequest, db: Session = Depends(get_db)):
    """生成麻醉須知"""
    # 檢查患者是否存在
    print("enter generate_guideline", request.patient_id)
    patient = db.query(Patient).filter(Patient.id == request.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    try:
        service = AnesthesiaGuidelineService()
        guideline = await service.generate_guideline(db, request)
        return guideline
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成麻醉須知失敗: {str(e)}"
        )


@router.get("/guidelines", response_model=List[AnesthesiaGuidelineResponse])
async def get_guidelines(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """獲取所有麻醉須知"""
    guidelines = db.query(AnesthesiaGuideline).offset(skip).limit(limit).all()
    return guidelines


@router.get("/guidelines/{guideline_id}", response_model=AnesthesiaGuidelineResponse)
async def get_guideline(guideline_id: int, db: Session = Depends(get_db)):
    """獲取特定麻醉須知"""
    guideline = db.query(AnesthesiaGuideline).filter(
        AnesthesiaGuideline.id == guideline_id
    ).first()
    
    if not guideline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="麻醉須知不存在"
        )
    
    return guideline


@router.put("/guidelines/{guideline_id}", response_model=AnesthesiaGuidelineResponse)
async def update_guideline(
    guideline_id: int, 
    guideline_update: AnesthesiaGuidelineUpdate, 
    db: Session = Depends(get_db)
):
    """更新麻醉須知"""
    guideline = db.query(AnesthesiaGuideline).filter(
        AnesthesiaGuideline.id == guideline_id
    ).first()
    
    if not guideline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="麻醉須知不存在"
        )
    
    update_data = guideline_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(guideline, field, value)
    
    db.commit()
    db.refresh(guideline)
    
    return guideline


@router.delete("/guidelines/{guideline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guideline(guideline_id: int, db: Session = Depends(get_db)):
    """刪除麻醉須知"""
    guideline = db.query(AnesthesiaGuideline).filter(
        AnesthesiaGuideline.id == guideline_id
    ).first()
    
    if not guideline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="麻醉須知不存在"
        )
    
    db.delete(guideline)
    db.commit()


@router.get("/guidelines/patient/{patient_id}", response_model=List[AnesthesiaGuidelineResponse])
async def get_patient_guidelines(patient_id: int, db: Session = Depends(get_db)):
    """獲取特定患者的所有麻醉須知"""
    # 檢查患者是否存在
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    guidelines = db.query(AnesthesiaGuideline).filter(
        AnesthesiaGuideline.patient_id == patient_id
    ).all()
    
    return guidelines


@router.get("/guidelines/by-date", response_model=List[AnesthesiaGuidelineResponse])
async def get_guidelines_by_date(
    surgery_date: date = Query(..., description="手術日期"),
    db: Session = Depends(get_db)
):
    """根據手術日期查詢麻醉須知"""
    guidelines = db.query(AnesthesiaGuideline).filter(
        AnesthesiaGuideline.surgery_date == surgery_date
    ).all()
    
    return guidelines


@router.get("/templates", response_model=List[AnesthesiaGuidelineTemplateResponse])
async def get_templates(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """獲取所有麻醉須知模板"""
    templates = db.query(AnesthesiaGuidelineTemplate).filter(
        AnesthesiaGuidelineTemplate.is_active == True
    ).offset(skip).limit(limit).all()
    
    return templates


@router.get("/templates/{template_id}", response_model=AnesthesiaGuidelineTemplateResponse)
async def get_template(template_id: int, db: Session = Depends(get_db)):
    """獲取特定麻醉須知模板"""
    template = db.query(AnesthesiaGuidelineTemplate).filter(
        AnesthesiaGuidelineTemplate.id == template_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模板不存在"
        )
    
    return template


@router.post("/templates", response_model=AnesthesiaGuidelineTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template: AnesthesiaGuidelineTemplateCreate, 
    db: Session = Depends(get_db)
):
    """建立麻醉須知模板"""
    db_template = AnesthesiaGuidelineTemplate(**template.dict())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    return db_template


@router.put("/templates/{template_id}", response_model=AnesthesiaGuidelineTemplateResponse)
async def update_template(
    template_id: int, 
    template_update: AnesthesiaGuidelineTemplateUpdate, 
    db: Session = Depends(get_db)
):
    """更新麻醉須知模板"""
    template = db.query(AnesthesiaGuidelineTemplate).filter(
        AnesthesiaGuidelineTemplate.id == template_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模板不存在"
        )
    
    update_data = template_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    
    return template


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(template_id: int, db: Session = Depends(get_db)):
    """刪除麻醉須知模板"""
    template = db.query(AnesthesiaGuidelineTemplate).filter(
        AnesthesiaGuidelineTemplate.id == template_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模板不存在"
        )
    
    db.delete(template)
    db.commit()


@router.get("/templates/by-type", response_model=List[AnesthesiaGuidelineTemplateResponse])
async def get_templates_by_type(
    anesthesia_type: str = Query(..., description="麻醉類型"),
    db: Session = Depends(get_db)
):
    """根據麻醉類型獲取模板"""
    templates = db.query(AnesthesiaGuidelineTemplate).filter(
        AnesthesiaGuidelineTemplate.anesthesia_type == anesthesia_type,
        AnesthesiaGuidelineTemplate.is_active == True
    ).all()
    
    return templates
