# Quick Start Guide - Anesthesia Management System

This guide will help you get the rebuilt Next.js + FastAPI application up and running quickly.

## Overview

The application has been completely rebuilt with:
- **Frontend**: Next.js 14 + shadcn/ui + Tailwind CSS (in `frontend-next/`)
- **Backend**: FastAPI (unchanged, in `backend/`)

## Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

## Quick Start

### 1. Start the Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### 2. Start the Frontend

Open a new terminal:

```bash
# Navigate to the new frontend directory
cd frontend-next

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## First Time Setup

### Backend Configuration

Create a `.env` file in the `backend/` directory:

```env
# Choose your LLM option
USE_LOCAL_LLM=false
OPENAI_API_KEY=your_openai_api_key_here

# OR use local LLM (Ollama)
# USE_LOCAL_LLM=true
# OLLAMA_URL=http://localhost:11434
# OLLAMA_MODEL=qwen2.5:7b

# Database
DATABASE_URL=sqlite:///./anesthesia.db

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### Frontend Configuration

Create a `.env.local` file in the `frontend-next/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Using the Application

### 1. Access Dashboard
- Open `http://localhost:3000`
- You'll see the dashboard with statistics and quick actions

### 2. Create a Patient
- Click "Create Patient" from the dashboard or navigation
- Fill in the patient information form
- Submit to create the patient

### 3. Generate Anesthesia Guideline
- Click "Generate Guideline" from the dashboard or navigation
- Follow the 3-step wizard:
  1. Select a patient
  2. Enter surgery details
  3. Review and confirm
- Click "Generate Guideline" to use AI to create the guideline

### 4. View Patient Details
- Navigate to "Patients" page
- Click "View" on any patient
- Explore tabs: Details, Medical History, Surgeries, Guidelines

## Key Features

### Dashboard
- Total patients and guidelines count
- Recent patients list
- Recent guidelines list
- Quick action buttons

### Patient Management
- Create, view, update, delete patients
- Search patients by name or insurance number
- View detailed patient information with tabs
- Track medical history and surgery records

### Guideline Generation
- Multi-step form for easy data entry
- AI-powered guideline generation
- View generated guidelines with detailed sections
- Link guidelines to patients

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Technology Stack

### Frontend
- **Next.js 14**: React framework with App Router
- **shadcn/ui**: High-quality UI components
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Data fetching and caching
- **React Hook Form**: Form handling
- **Zod**: Schema validation
- **Axios**: HTTP client
- **TypeScript**: Type safety

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation
- **OpenAI API / Ollama**: AI-powered guideline generation
- **SQLite**: Database (default)

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.8+)
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip list`

### Frontend won't start
- Check Node version: `node --version` (should be 18+)
- Delete `node_modules` and `.next`: `rm -rf node_modules .next`
- Reinstall: `npm install`

### Can't connect to API
- Ensure backend is running on port 8000
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Verify CORS settings in backend allow `http://localhost:3000`

### AI generation not working
- Check your `.env` file in backend directory
- Verify `OPENAI_API_KEY` is set (if using OpenAI)
- Or ensure Ollama is running (if using local LLM)

## Project Structure

```
anesthesia/
├── frontend-next/          # NEW Next.js frontend
│   ├── src/
│   │   ├── app/           # Pages (App Router)
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities, API, hooks
│   │   └── types/         # TypeScript types
│   └── package.json
├── backend/               # FastAPI backend (unchanged)
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   └── requirements.txt
└── frontend/             # OLD React frontend (can be removed)
```

## Next Steps

1. Explore the dashboard and create some test data
2. Try generating an AI-powered guideline
3. Customize the UI by modifying Tailwind config
4. Add more components using `npx shadcn@latest add [component]`
5. Extend the API with new endpoints as needed

## Support

For issues or questions:
- Check the README files in each directory
- Review the API documentation at `http://localhost:8000/docs`
- Inspect browser console for frontend errors
- Check backend logs for API errors

## Development Mode

Both servers support hot-reload:
- Frontend: Changes to React components reload automatically
- Backend: Changes to Python files reload automatically (with `--reload` flag)

Happy coding!
