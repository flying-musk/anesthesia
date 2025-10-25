"""
Anesthesia guidelines-related API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Union
from datetime import date

from app.core.database import get_db
from app.models.anesthesia import AnesthesiaGuideline, AnesthesiaGuidelineTemplate
from app.models.patient import Patient
from app.schemas.anesthesia import (
    AnesthesiaGuidelineCreate, AnesthesiaGuidelineUpdate, AnesthesiaGuidelineResponse,
    AnesthesiaGuidelineTemplateCreate, AnesthesiaGuidelineTemplateUpdate,
    AnesthesiaGuidelineTemplateResponse, GenerateGuidelineRequest,
    AnesthesiaGuidelineWithPatient, LanguageEnum
)
from app.schemas.patient import PaginatedResponse
from app.services.anesthesia_service import AnesthesiaGuidelineService
from math import ceil

router = APIRouter()


@router.post("/guidelines/generate", response_model=Union[AnesthesiaGuidelineResponse, List[AnesthesiaGuidelineResponse]], status_code=status.HTTP_201_CREATED)
async def generate_guideline(request: GenerateGuidelineRequest, db: Session = Depends(get_db)):
    """Generate anesthesia guideline in multiple languages (always generates all 3 languages, returns requested language or all)"""
    # Check if patient exists
    print("enter generate_guideline", request.patient_id)
    patient = db.query(Patient).filter(Patient.id == request.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    try:
        service = AnesthesiaGuidelineService()
        guidelines = await service.generate_guideline_multilingual(db, request)
        return guidelines
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate anesthesia guideline: {str(e)}"
        )


@router.get("/guidelines", response_model=PaginatedResponse[AnesthesiaGuidelineResponse])
async def get_guidelines(
    page: int = 1,
    size: int = 100,
    language: Optional[LanguageEnum] = Query(None, description="Filter by language"),
    db: Session = Depends(get_db)
):
    """Get all anesthesia guidelines with pagination"""
    # Calculate offset
    skip = (page - 1) * size

    # Build query
    query = db.query(AnesthesiaGuideline)
    if language:
        query = query.filter(AnesthesiaGuideline.language == language.value)

    # Get total count
    total = query.count()

    # Get guidelines for current page
    guidelines = query.offset(skip).limit(size).all()

    # Calculate total pages
    pages = ceil(total / size) if size > 0 else 0

    return PaginatedResponse(
        items=guidelines,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/guidelines/{guideline_id}", response_model=AnesthesiaGuidelineResponse)
async def get_guideline(
    guideline_id: int, 
    language: Optional[LanguageEnum] = Query(None, description="Language preference"),
    db: Session = Depends(get_db)
):
    """Get specific anesthesia guideline"""
    # First, get the guideline to find its group_id
    original_guideline = db.query(AnesthesiaGuideline).filter(AnesthesiaGuideline.id == guideline_id).first()
    
    if not original_guideline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anesthesia guideline not found"
        )
    
    # If language is specified, find the guideline with the same group_id and language
    if language:
        guideline = db.query(AnesthesiaGuideline).filter(
            AnesthesiaGuideline.group_id == original_guideline.group_id,
            AnesthesiaGuideline.language == language.value
        ).first()
        
        if not guideline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Anesthesia guideline not found in language: {language.value}"
            )
    else:
        # Return the original guideline if no language specified
        guideline = original_guideline

    return guideline


@router.put("/guidelines/{guideline_id}", response_model=AnesthesiaGuidelineResponse)
async def update_guideline(
    guideline_id: int,
    guideline_update: AnesthesiaGuidelineUpdate,
    db: Session = Depends(get_db)
):
    """Update anesthesia guideline"""
    guideline = db.query(AnesthesiaGuideline).filter(
        AnesthesiaGuideline.id == guideline_id
    ).first()

    if not guideline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anesthesia guideline not found"
        )
    
    update_data = guideline_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(guideline, field, value)
    
    db.commit()
    db.refresh(guideline)
    
    return guideline


@router.delete("/guidelines/{guideline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guideline(guideline_id: int, db: Session = Depends(get_db)):
    """Delete anesthesia guideline"""
    guideline = db.query(AnesthesiaGuideline).filter(
        AnesthesiaGuideline.id == guideline_id
    ).first()

    if not guideline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anesthesia guideline not found"
        )
    
    db.delete(guideline)
    db.commit()


@router.get("/guidelines/patient/{patient_id}", response_model=List[AnesthesiaGuidelineResponse])
async def get_patient_guidelines(
    patient_id: int, 
    language: Optional[LanguageEnum] = Query(None, description="Filter by language"),
    db: Session = Depends(get_db)
):
    """Get all anesthesia guidelines for a specific patient"""
    # Check if patient exists
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    query = db.query(AnesthesiaGuideline).filter(AnesthesiaGuideline.patient_id == patient_id)
    
    if language:
        query = query.filter(AnesthesiaGuideline.language == language.value)
    
    guidelines = query.all()
    
    return guidelines


@router.get("/guidelines/by-date", response_model=List[AnesthesiaGuidelineResponse])
async def get_guidelines_by_date(
    surgery_date: date = Query(..., description="Surgery date"),
    language: Optional[LanguageEnum] = Query(None, description="Filter by language"),
    db: Session = Depends(get_db)
):
    """Get anesthesia guidelines by surgery date"""
    query = db.query(AnesthesiaGuideline).filter(AnesthesiaGuideline.surgery_date == surgery_date)
    
    if language:
        query = query.filter(AnesthesiaGuideline.language == language.value)
    
    guidelines = query.all()

    return guidelines


@router.get("/templates", response_model=List[AnesthesiaGuidelineTemplateResponse])
async def get_templates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all anesthesia guideline templates"""
    templates = db.query(AnesthesiaGuidelineTemplate).filter(
        AnesthesiaGuidelineTemplate.is_active == True
    ).offset(skip).limit(limit).all()

    return templates


@router.get("/templates/{template_id}", response_model=AnesthesiaGuidelineTemplateResponse)
async def get_template(template_id: int, db: Session = Depends(get_db)):
    """Get specific anesthesia guideline template"""
    template = db.query(AnesthesiaGuidelineTemplate).filter(
        AnesthesiaGuidelineTemplate.id == template_id
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    return template


@router.post("/templates", response_model=AnesthesiaGuidelineTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template: AnesthesiaGuidelineTemplateCreate,
    db: Session = Depends(get_db)
):
    """Create anesthesia guideline template"""
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
    """Update anesthesia guideline template"""
    template = db.query(AnesthesiaGuidelineTemplate).filter(
        AnesthesiaGuidelineTemplate.id == template_id
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    update_data = template_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    
    return template


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(template_id: int, db: Session = Depends(get_db)):
    """Delete anesthesia guideline template"""
    template = db.query(AnesthesiaGuidelineTemplate).filter(
        AnesthesiaGuidelineTemplate.id == template_id
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    db.delete(template)
    db.commit()


@router.get("/templates/by-type", response_model=List[AnesthesiaGuidelineTemplateResponse])
async def get_templates_by_type(
    anesthesia_type: str = Query(..., description="Anesthesia type"),
    db: Session = Depends(get_db)
):
    """Get templates by anesthesia type"""
    templates = db.query(AnesthesiaGuidelineTemplate).filter(
        AnesthesiaGuidelineTemplate.anesthesia_type == anesthesia_type,
        AnesthesiaGuidelineTemplate.is_active == True
    ).all()

    return templates
