# 🏥 AI-Powered Anesthesia Guidelines Generation System

An AI-based personalized anesthesia guidelines generation system with multi-language support (Chinese, English, French).

## 📁 Project Structure

```
anesthesia/
├── frontend-next/           # Next.js frontend application
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── i18n/           # Internationalization config
│   │   └── ...
│   ├── package.json
│   └── ...
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   ├── scripts/            # Script files
│   ├── requirements.txt
│   └── ...
├── README.md
└── ...
```

## 🚀 Quick Start

### 1. Start Backend Service
```bash
cd backend
py -3.10 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python start_demo.py
uvicorn app.main:app --reload
```

### 2. Start Frontend Service

```bash
cd frontend-next
npm install
npm run dev
```

### 3. Access the System

- **Frontend Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🌍 Multi-Language Support

The system supports three languages:
- 🇹🇼 繁體中文 (zh-TW)
- 🇺🇸 English (en-US)
- 🇫🇷 Français (fr-FR)

Users can switch languages using the language selector in the top-right corner.

## 🎯 Key Features

### Frontend Features
- ✅ Multi-language interface support
- ✅ Patient management (create, search, view, edit)
- ✅ Anesthesia guidelines generation
- ✅ Responsive design
- ✅ Modern UI interface

### Backend Features
- ✅ RESTful API
- ✅ Patient management system
- ✅ Medical history management
- ✅ AI anesthesia guidelines generation
- ✅ Local LLM support (Ollama)
- ✅ OpenAI API integration

## 🛠️ Tech Stack

### Frontend
- Next.js 14
- React 18
- Material-UI (MUI)
- React Hook Form
- i18next (Internationalization)
- Axios

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- OpenAI API
- Ollama (Local LLM)
- Pydantic

## 📋 API Endpoints

### Patient Management
- `GET /api/v1/patients/` - Get all patients
- `POST /api/v1/patients/` - Create patient
- `GET /api/v1/patients/{id}` - Get patient details
- `PUT /api/v1/patients/{id}` - Update patient
- `DELETE /api/v1/patients/{id}` - Delete patient
- `POST /api/v1/patients/search` - Search patients

### Anesthesia Guidelines
- `POST /api/v1/anesthesia/guidelines/generate` - Generate anesthesia guidelines
- `GET /api/v1/anesthesia/guidelines/` - Get all anesthesia guidelines
- `GET /api/v1/anesthesia/guidelines/{id}` - Get anesthesia guideline details
- `PUT /api/v1/anesthesia/guidelines/{id}` - Update anesthesia guideline
- `DELETE /api/v1/anesthesia/guidelines/{id}` - Delete anesthesia guideline

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# Use local LLM (Ollama)
USE_LOCAL_LLM=true
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# Or use OpenAI
OPENAI_API_KEY=your_api_key_here
USE_LOCAL_LLM=false

# Other settings
DEBUG=true
DATABASE_URL=sqlite:///./anesthesia.db
```

### Local LLM Setup

1. Install Ollama
2. Download model: `ollama pull qwen2.5:7b`
3. Start service: `ollama serve`
4. Set environment variable: `USE_LOCAL_LLM=true`

## 🧪 Testing

### Backend Testing
```bash
cd backend
python scripts/test_api.py
```

### Frontend Testing
```bash
cd frontend-next
npm test
```

## 📚 Documentation

- [Quick Start Guide](QUICK_START.md)
- [Local LLM Setup Guide](LOCAL_LLM_GUIDE.md)
- [API Documentation](http://localhost:8000/docs)

---