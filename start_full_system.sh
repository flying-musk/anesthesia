#!/bin/bash

echo "🚀 Starting Anesthesia Management System (Full Version)"
echo "=================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed, please install Node.js first"
    echo "💡 Download: https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed, please install Python3 first"
    exit 1
fi

echo "✅ Environment check completed"

# Start backend
echo "📡 Starting backend service..."
cd backend
python3 start_demo.py
echo "✅ Backend initialization completed"

# Start backend server in background
echo "🚀 Starting FastAPI server..."
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
echo "✅ Backend service started (PID: $BACKEND_PID)"

# Wait for backend to start
echo "⏳ Waiting for backend service to start..."
sleep 5

# Check if backend is running properly
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend service running normally"
else
    echo "❌ Backend service failed to start"
    kill $BACKEND_PID
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend service..."
cd ../frontend-next

# Check if dependencies need to be installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

echo "🚀 Starting Next.js development server..."
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend service started (PID: $FRONTEND_PID)"

echo ""
echo "🎉 System startup completed!"
echo "=================================================="
echo "📱 Frontend UI: http://localhost:3000"
echo "📡 API Docs: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "🌍 Supported Languages:"
echo "  - 🇹🇼 Traditional Chinese"
echo "  - 🇺🇸 English"
echo "  - 🇫🇷 Français"
echo ""
echo "🛑 Stop Services:"
echo "  - Press Ctrl+C to stop frontend"
echo "  - Run 'kill $BACKEND_PID' to stop backend"
echo ""

# Wait for user interrupt
wait $FRONTEND_PID
