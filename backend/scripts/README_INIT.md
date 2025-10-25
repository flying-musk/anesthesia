# Multilingual System Initialization

This directory contains scripts for initializing the anesthesia management system with complete multilingual support.

## 🚀 Quick Start

### Option 1: Automated Script (Recommended)
```bash
cd backend
./scripts/init_complete_system.sh
```

### Option 2: Manual Python Script
```bash
cd backend
python3 scripts/init_multilingual_system.py
```

## 📋 What Gets Initialized

### Database Setup
- ✅ Creates all required database tables
- ✅ Adds multilingual columns (`language`, `group_id`) to existing tables
- ✅ Creates necessary indexes for performance

### Sample Data Creation
- ✅ **Anesthesia Templates**: 4 templates (general, local, regional, sedation)
- ✅ **Sample Patients**: 3 patients with complete profiles
- ✅ **Medical Histories**: Multilingual (EN/ZH/FR) for each patient
- ✅ **Surgery Records**: Multilingual (EN/ZH/FR) for each patient
- ✅ **Anesthesia Guidelines**: Sample guidelines in all languages

### Multilingual Support
- 🌐 **English (EN)**: Original language
- 🌐 **Chinese (ZH)**: AI-translated medical content
- 🌐 **French (FR)**: AI-translated medical content

## 🔧 Available Scripts

### Core Initialization
- `init_multilingual_system.py` - Complete system initialization
- `init_complete_system.sh` - Automated shell script wrapper

### Migration Scripts
- `migrate_multilingual.py` - Add language support to anesthesia guidelines
- `migrate_medical_multilingual.py` - Add language support to medical records
- `migrate_group_id.py` - Add group_id for multilingual associations

### Sample Data
- `init_multilingual_sample_data.py` - Create multilingual sample data
- `init_sample_data.py` - Legacy sample data (English only)

### Testing & Verification
- `test_multilingual.py` - Test multilingual API endpoints
- `test_medical_multilingual.py` - Test medical record multilingual features
- `check_medical_data.py` - Verify data integrity

## 📊 Data Structure

### Patients
- **John Smith** (Insurance: 1234567890)
  - Medical History: Hypertension, Penicillin allergy
  - Surgery Records: Cataract surgery, Gallbladder removal
- **Emily Johnson** (Insurance: 0987654321)
  - Medical History: Asthma, Latex allergy
  - Surgery Records: Tonsillectomy
- **Michael Chen** (Insurance: 1122334455)
  - Medical History: Diabetes Type 2, Shellfish allergy
  - Surgery Records: Gallbladder removal, Appendectomy

### Language Distribution
Each medical record and surgery record is created in 3 languages:
- **English**: Original content
- **Chinese**: AI-translated with medical terminology
- **French**: AI-translated with medical terminology

## 🌐 API Usage Examples

### Get Patient Details by Language
```bash
# English (default)
curl "http://localhost:8000/api/v1/patients/1"

# Chinese
curl "http://localhost:8000/api/v1/patients/1?language=zh"

# French
curl "http://localhost:8000/api/v1/patients/1?language=fr"
```

### Get Medical History by Language
```bash
# English
curl "http://localhost:8000/api/v1/patients/1/medical-history?language=en"

# Chinese
curl "http://localhost:8000/api/v1/patients/1/medical-history?language=zh"

# French
curl "http://localhost:8000/api/v1/patients/1/medical-history?language=fr"
```

### Get Surgery Records by Language
```bash
# English
curl "http://localhost:8000/api/v1/patients/1/surgery-records?language=en"

# Chinese
curl "http://localhost:8000/api/v1/patients/1/surgery-records?language=zh"

# French
curl "http://localhost:8000/api/v1/patients/1/surgery-records?language=fr"
```

### Create New Records (Auto-translates to all languages)
```bash
# Create medical history (creates EN/ZH/FR versions)
curl -X POST "http://localhost:8000/api/v1/patients/1/medical-history" \
  -H "Content-Type: application/json" \
  -d '{
    "allergies": "Peanut allergy",
    "chronic_conditions": "Diabetes",
    "current_medications": "Metformin",
    "language": "en"
  }'

# Create surgery record (creates EN/ZH/FR versions)
curl -X POST "http://localhost:8000/api/v1/patients/1/surgery-records" \
  -H "Content-Type: application/json" \
  -d '{
    "surgery_name": "Heart Surgery",
    "surgery_type": "general",
    "surgery_date": "2025-01-25",
    "surgeon_name": "Dr. Heart Specialist",
    "anesthesiologist_name": "Dr. Anesthesia Expert",
    "language": "en"
  }'
```

## 🔍 Verification

After initialization, verify the system is working:

```bash
# Check total records
python3 scripts/check_medical_data.py

# Test API endpoints
python3 scripts/test_medical_multilingual.py

# Test anesthesia guidelines
python3 scripts/test_multilingual.py
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure SQLite database file is writable
   - Check file permissions in the backend directory

2. **Translation Errors**
   - Ollama service is optional (falls back to mock translation)
   - Mock translation provides basic medical terminology

3. **Missing Dependencies**
   - Run: `pip install -r requirements.txt`
   - Ensure Python 3.8+ is installed

4. **Permission Errors**
   - Make scripts executable: `chmod +x scripts/*.sh`
   - Run from the backend directory

### Reset Database
To start fresh:
```bash
rm anesthesia.db
python3 scripts/init_multilingual_system.py
```

## 📈 Performance Notes

- Initialization creates ~50-100 database records
- Translation process may take 1-2 minutes
- Database size: ~2-5 MB after initialization
- API response time: <100ms for most endpoints

## 🔄 Updates

To update existing data with new multilingual features:
```bash
# Fix existing medical data
python3 scripts/fix_existing_medical_data.py

# Regenerate translations
python3 scripts/regenerate_medical_translations.py
python3 scripts/regenerate_surgery_translations.py
```
