#!/usr/bin/env python
"""
API Test Script - FastAPI Version
For testing the Anesthesia Management System API endpoints
"""

import asyncio
import httpx
import json
from datetime import date

# API Base URL
BASE_URL = 'http://localhost:8000/api/v1'


async def test_patient_search():
    """Test patient search"""
    print("Testing patient search...")

    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/patients/search"
        data = {
            "health_insurance_number": "1234567890",
            "full_name": "John Smith",
            "date_of_birth": "1985-05-15"
        }

        response = await client.post(url, json=data)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            patient_data = response.json()
            print(f"Found patient: {patient_data['full_name']}")
            return patient_data['id']
        else:
            print(f"Error: {response.text}")
            return None


async def test_generate_guideline(patient_id):
    """Test anesthesia guideline generation"""
    print("Testing anesthesia guideline generation...")

    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/anesthesia/guidelines/generate"
        data = {
            "patient_id": patient_id,
            "surgery_name": "Laparoscopic Cholecystectomy",
            "anesthesia_type": "general",
            "surgery_date": "2024-01-15",
            "surgeon_name": "Dr. Lee",
            "anesthesiologist_name": "Dr. Chen"
        }

        response = await client.post(url, json=data)
        print(f"Status code: {response.status_code}")
        if response.status_code == 201:
            guideline_data = response.json()
            print("Anesthesia guideline generated successfully!")
            print(f"Surgery name: {guideline_data['surgery_name']}")
            print(f"Anesthesia type: {guideline_data['anesthesia_type']}")
            print(f"Is generated: {guideline_data['is_generated']}")
            return guideline_data['id']
        else:
            print(f"Error: {response.text}")
            return None


async def test_get_guideline(guideline_id):
    """Test getting anesthesia guideline"""
    print("Testing getting anesthesia guideline...")

    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/anesthesia/guidelines/{guideline_id}"
        response = await client.get(url)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            guideline_data = response.json()
            print("Anesthesia guideline content:")
            print(f"- Anesthesia type info: {guideline_data['anesthesia_type_info'][:100]}...")
            print(f"- Surgery process: {guideline_data['surgery_process'][:100]}...")
            print(f"- Expected sensations: {guideline_data['expected_sensations'][:100]}...")
            print(f"- Potential risks: {guideline_data['potential_risks'][:100]}...")
            print(f"- Pre-surgery instructions: {guideline_data['pre_surgery_instructions'][:100]}...")
            print(f"- Fasting instructions: {guideline_data['fasting_instructions'][:100]}...")
            print(f"- Medication instructions: {guideline_data['medication_instructions'][:100]}...")
            print(f"- Common questions: {guideline_data['common_questions'][:100]}...")
            print(f"- Post-surgery care: {guideline_data['post_surgery_care'][:100]}...")
        else:
            print(f"Error: {response.text}")


async def test_get_patient_guidelines(patient_id):
    """Test getting all patient anesthesia guidelines"""
    print("Testing getting all patient anesthesia guidelines...")

    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/anesthesia/guidelines/patient/{patient_id}"
        response = await client.get(url)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            guidelines = response.json()
            print(f"Patient has {len(guidelines)} anesthesia guidelines")
            for guideline in guidelines:
                print(f"- {guideline['surgery_name']} ({guideline['surgery_date']})")
        else:
            print(f"Error: {response.text}")


async def test_health_check():
    """Test health check"""
    print("Testing health check...")

    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL.replace('/api/v1', '')}/health"
        response = await client.get(url)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"Health status: {health_data['status']}")
        else:
            print(f"Error: {response.text}")


async def main():
    """Main function"""
    print("Starting FastAPI tests...")
    print("=" * 50)

    # Test health check
    await test_health_check()
    print("=" * 50)

    # Test patient search
    patient_id = await test_patient_search()
    if not patient_id:
        print("Patient search failed, cannot continue testing")
        return

    print("=" * 50)

    # Test anesthesia guideline generation
    guideline_id = await test_generate_guideline(patient_id)
    if not guideline_id:
        print("Anesthesia guideline generation failed, cannot continue testing")
        return

    print("=" * 50)

    # Test getting anesthesia guideline
    await test_get_guideline(guideline_id)

    print("=" * 50)

    # Test getting all patient anesthesia guidelines
    await test_get_patient_guidelines(patient_id)

    print("=" * 50)
    print("FastAPI tests completed!")


if __name__ == '__main__':
    asyncio.run(main())