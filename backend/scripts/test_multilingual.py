#!/usr/bin/env python3
"""
Test script for multilingual anesthesia guideline generation
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import date

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.models.patient import Patient
from app.schemas.anesthesia import GenerateGuidelineRequest, LanguageEnum, AnesthesiaTypeEnum
from app.services.anesthesia_service import AnesthesiaGuidelineService
from loguru import logger

async def test_multilingual_generation():
    """Test multilingual guideline generation"""
    db = SessionLocal()
    
    try:
        # Create a test patient if not exists
        test_patient = db.query(Patient).filter(Patient.full_name == "Test Patient").first()
        if not test_patient:
            test_patient = Patient(
                full_name="Test Patient",
                date_of_birth=date(1990, 1, 1),
                gender="M",
                health_insurance_number="TEST123456"
            )
            db.add(test_patient)
            db.commit()
            db.refresh(test_patient)
            logger.info(f"Created test patient with ID: {test_patient.id}")
        
        # Create test request - will generate all 3 languages but return all
        request = GenerateGuidelineRequest(
            patient_id=test_patient.id,
            surgery_name="Test Surgery",
            anesthesia_type=AnesthesiaTypeEnum.GENERAL,
            surgery_date=date.today(),
            surgeon_name="Dr. Test",
            anesthesiologist_name="Dr. Anesthesia"
            # return_language not specified, so will return all languages
        )
        
        # Generate guidelines
        service = AnesthesiaGuidelineService()
        guidelines = await service.generate_guideline_multilingual(db, request)
        
        logger.info(f"Generated {len(guidelines)} guidelines:")
        for guideline in guidelines:
            logger.info(f"- ID: {guideline.id}, Language: {guideline.language}, Surgery: {guideline.surgery_name}")
            logger.info(f"  Anesthesia Type Info: {guideline.anesthesia_type_info[:100]}...")
        
        return guidelines
        
    except Exception as e:
        logger.error(f"Error during test: {str(e)}")
        raise
    finally:
        db.close()

async def test_single_language_generation():
    """Test single language guideline generation"""
    db = SessionLocal()
    
    try:
        # Get existing test patient
        test_patient = db.query(Patient).filter(Patient.full_name == "Test Patient").first()
        if not test_patient:
            logger.error("Test patient not found. Please run test_multilingual_generation first.")
            return
        
        # Create test request for single language - will generate all 3 languages but return only Chinese
        request = GenerateGuidelineRequest(
            patient_id=test_patient.id,
            surgery_name="Single Language Test Surgery",
            anesthesia_type=AnesthesiaTypeEnum.LOCAL,
            surgery_date=date.today(),
            surgeon_name="Dr. Single",
            anesthesiologist_name="Dr. Local",
            return_language=LanguageEnum.ZH  # Only return Chinese version
        )
        
        # Generate guidelines
        service = AnesthesiaGuidelineService()
        guidelines = await service.generate_guideline_multilingual(db, request)
        
        logger.info(f"Generated {len(guidelines)} guidelines for single language:")
        for guideline in guidelines:
            logger.info(f"- ID: {guideline.id}, Language: {guideline.language}, Surgery: {guideline.surgery_name}")
            logger.info(f"  Anesthesia Type Info: {guideline.anesthesia_type_info[:100]}...")
        
        return guidelines
        
    except Exception as e:
        logger.error(f"Error during test: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test multilingual anesthesia guideline generation")
    parser.add_argument("--single", action="store_true", help="Test single language generation")
    
    args = parser.parse_args()
    
    if args.single:
        asyncio.run(test_single_language_generation())
    else:
        asyncio.run(test_multilingual_generation())
