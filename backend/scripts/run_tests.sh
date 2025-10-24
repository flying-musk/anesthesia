#!/bin/bash

# 麻醉須知系統測試腳本 - FastAPI 版本 (SQLite)

echo "麻醉須知系統測試腳本 (FastAPI + SQLite)"
echo "======================================="

# 檢查 Python 是否已安裝
if ! command -v python &> /dev/null; then
    echo "錯誤: Python 未安裝"
    exit 1
fi

# 檢查是否在虛擬環境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "警告: 建議在虛擬環境中運行"
fi

# 安裝依賴
echo "安裝依賴..."
pip install -r requirements.txt

# 初始化資料庫和 demo 資料
echo "初始化 SQLite 資料庫和 demo 資料..."
python start_demo.py

# 啟動開發伺服器（背景執行）
echo "啟動 FastAPI 開發伺服器..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
SERVER_PID=$!

# 等待伺服器啟動
echo "等待伺服器啟動..."
sleep 5

# 測試 API
echo "測試 API..."
python scripts/test_api.py

# 停止伺服器
echo "停止伺服器..."
kill $SERVER_PID

echo "測試完成！"
echo ""
echo "使用說明："
echo "1. 啟動伺服器: uvicorn app.main:app --reload"
echo "2. API 文檔: http://localhost:8000/docs"
echo "3. ReDoc 文檔: http://localhost:8000/redoc"
echo "4. 測試 API: python scripts/test_api.py"