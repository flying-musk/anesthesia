# 🚀 Quick Start Guide (Hackathon Demo)

## One-Click Start (Recommended)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize SQLite database and demo data
python start_demo.py

# 3. Start the server
uvicorn app.main:app --reload
```

## Accessing the System

  - **API Documentation**: http://localhost:8000/docs
  - **ReDoc Documentation**: http://localhost:8000/redoc
  - **Health Check**: http://localhost:8000/health

## Demo Data

The system will automatically create the following demo data:

### Patient 1: John Smith

  - Health Insurance Number: `1234567890`
  - Name: `John Smith`
  - Date of Birth: `1985-05-15`
  - Gender: Male
  - Medical History: Penicillin allergy, Hypertension

### Patient 2: Emily Johnson

  - Health Insurance Number: `0987654321`
  - Name: `Emily Johnson`
  - Date of Birth: `1990-08-22`
  - Gender: Female
  - Medical History: No special medical history

## Testing the API

### 1\. Search Patients

```bash
curl -X POST "http://localhost:8000/api/v1/patients/search" \
  -H "Content-Type: application/json" \
  -d '{
    "health_insurance_number": "1234567890",
    "full_name": "John Smith",
    "date_of_birth": "1985-05-15"
  }'
```

### 2\. Generate Anesthesia Guidelines

```bash
curl -X POST "http://localhost:8000/api/v1/anesthesia/guidelines/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "surgery_name": "Laparoscopic Cholecystectomy",
    "anesthesia_type": "general",
    "surgery_date": "2024-01-15",
    "surgeon_name": "Dr. Smith",
    "anesthesiologist_name": "Dr. Johnson"
  }'
```

### 3\. Automated Testing

```bash
python scripts/test_api.py
```

## System Features

✅ **Zero Configuration**: Uses SQLite, no database installation required  
✅ **Quick Start**: One-click initialization for demo data  
✅ **Auto-Documentation**: Automatically generates API docs  
✅ **AI Integration**: Uses OpenAI GPT-4 to generate personalized guidelines  
✅ **Full-Featured**: Patient management, medical history, anesthesia guideline generation

## Troubleshooting

### If you encounter an OpenAI API error

1.  Set the environment variable: `export OPENAI_API_KEY=your_api_key_here`
2.  Or create a `.env` file and set `OPENAI_API_KEY=your_api_key_here`

### If the port is occupied

```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

## Production Deployment

For deployment to a production environment, it is recommended to:

1.  Use PostgreSQL instead of SQLite
2.  Set environment variables
3.  Use Gunicorn or Uvicorn as the WSGI server

-----

🎯 **Hackathon Prep Complete\!** Now you can focus on front-end development and system integration\!