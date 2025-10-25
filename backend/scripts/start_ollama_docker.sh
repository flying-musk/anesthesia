#!/bin/bash

echo "🐳 啟動Ollama Docker容器..."

# 檢查Docker是否運行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未運行，請先啟動Docker Desktop"
    echo "💡 安裝Docker Desktop: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# 啟動Ollama容器
echo "🚀 啟動Ollama容器..."
docker-compose up -d ollama

# 等待服務啟動
echo "⏳ 等待Ollama服務啟動..."
sleep 10

# 檢查服務狀態
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama服務已啟動"
    
    # 下載推薦的中文模型
    echo "📥 下載中文模型 qwen2.5:7b..."
    docker exec ollama ollama pull qwen2.5:7b
    
    echo "🎉 Ollama設定完成！"
    echo "📋 可用模型："
    docker exec ollama ollama list
    
    echo ""
    echo "🔧 現在你可以："
    echo "1. 設定環境變數: export USE_LOCAL_LLM=true"
    echo "2. 測試連接: python3 scripts/test_ollama.py"
    echo "3. 啟動你的麻醉系統: uvicorn app.main:app --reload"
    
else
    echo "❌ Ollama服務啟動失敗"
    echo "💡 請檢查Docker容器狀態: docker ps"
fi
