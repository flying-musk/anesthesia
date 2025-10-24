#!/bin/bash

echo "🚀 啟動麻醉前須知生成系統 (完整版)"
echo "=================================================="

# 檢查Node.js是否安裝
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安裝，請先安裝Node.js"
    echo "💡 下載地址: https://nodejs.org/"
    exit 1
fi

# 檢查Python是否安裝
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安裝，請先安裝Python3"
    exit 1
fi

echo "✅ 環境檢查完成"

# 啟動後端
echo "📡 啟動後端服務..."
cd backend
python3 start_demo.py
echo "✅ 後端初始化完成"

# 在後台啟動後端服務器
echo "🚀 啟動FastAPI服務器..."
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
echo "✅ 後端服務已啟動 (PID: $BACKEND_PID)"

# 等待後端啟動
echo "⏳ 等待後端服務啟動..."
sleep 5

# 檢查後端是否正常運行
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 後端服務運行正常"
else
    echo "❌ 後端服務啟動失敗"
    kill $BACKEND_PID
    exit 1
fi

# 啟動前端
echo "🎨 啟動前端服務..."
cd ../frontend-next

# 檢查是否需要安裝依賴
if [ ! -d "node_modules" ]; then
    echo "📦 安裝前端依賴..."
    npm install
fi

echo "🚀 啟動Next.js開發服務器..."
npm run dev &
FRONTEND_PID=$!
echo "✅ 前端服務已啟動 (PID: $FRONTEND_PID)"

echo ""
echo "🎉 系統啟動完成！"
echo "=================================================="
echo "📱 前端界面: http://localhost:3000"
echo "📡 API文檔: http://localhost:8000/docs"
echo "🔍 健康檢查: http://localhost:8000/health"
echo ""
echo "🌍 支援語言:"
echo "  - 🇹🇼 繁體中文"
echo "  - 🇺🇸 English"
echo "  - 🇫🇷 Français"
echo ""
echo "🛑 停止服務:"
echo "  - 按 Ctrl+C 停止前端"
echo "  - 運行 'kill $BACKEND_PID' 停止後端"
echo ""

# 等待用戶中斷
wait $FRONTEND_PID
