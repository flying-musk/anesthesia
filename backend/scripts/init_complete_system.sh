#!/bin/bash

# Complete Multilingual System Initialization Script
# This script initializes the entire anesthesia management system with multilingual support

echo "🚀 Starting Complete Multilingual System Initialization..."
echo "============================================================"

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "Usage: cd backend && ./scripts/init_complete_system.sh"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import sqlalchemy, fastapi, pydantic" 2>/dev/null || {
    echo "❌ Error: Required packages not installed"
    echo "Please run: pip install -r requirements.txt"
    exit 1
}

echo "✅ Dependencies check passed"

# Run the complete initialization
echo ""
echo "🔄 Running complete multilingual system initialization..."
echo "This may take a few minutes..."

python3 scripts/init_multilingual_system.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 System initialization completed successfully!"
    echo ""
    echo "📋 What was created:"
    echo "✅ Database tables with multilingual support"
    echo "✅ Anesthesia guideline templates"
    echo "✅ Sample patients with multilingual data"
    echo "✅ Medical histories in EN/ZH/FR"
    echo "✅ Surgery records in EN/ZH/FR"
    echo "✅ Anesthesia guidelines in EN/ZH/FR"
    echo ""
    echo "🌐 Supported Languages: English, Chinese, French"
    echo ""
    echo "🚀 You can now start the backend server:"
    echo "   python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
    echo "📖 API Documentation will be available at:"
    echo "   http://localhost:8000/docs"
else
    echo ""
    echo "❌ Initialization failed. Please check the error messages above."
    exit 1
fi
