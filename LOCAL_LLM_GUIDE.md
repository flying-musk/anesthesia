# 🚀 本地LLM設定指南 - 麻醉須知生成系統

## 📋 概述

你的麻醉須知生成系統現在支援本地LLM (Ollama)！這意味著你可以：

- ✅ **完全在本地運行AI功能**
- ✅ **不需要網路連線**
- ✅ **不需要OpenAI API費用**
- ✅ **完全控制AI模型和回應**

## 🛠️ 安裝Ollama

### 方法1: 手動下載 (推薦)

1. **下載Ollama**：
   - 訪問：https://ollama.ai/download
   - 下載macOS版本
   - 安裝到應用程式資料夾

2. **啟動Ollama服務**：
   ```bash
   ollama serve
   ```

3. **下載中文模型**：
   ```bash
   # 推薦的中文模型 (7B參數，約4GB)
   ollama pull qwen2.5:7b
   
   # 或者使用更小的模型 (3B參數，約2GB)
   ollama pull qwen2.5:3b
   
   # 或者使用英文模型 (如果需要)
   ollama pull llama3.1:7b
   ```

### 方法2: 使用Docker

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## ⚙️ 配置系統使用本地LLM

### 1. 創建環境配置文件

複製 `env.local.example` 為 `.env`：

```bash
cp env.local.example .env
```

### 2. 編輯 `.env` 文件

```bash
# 使用本地LLM (Ollama) 替代OpenAI
USE_LOCAL_LLM=true

# Ollama設定
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# OpenAI設定 (如果不使用本地LLM)
OPENAI_API_KEY=your_openai_api_key_here

# 其他設定
DEBUG=true
DATABASE_URL=sqlite:///./anesthesia.db
SECRET_KEY=your-secret-key-here
```

### 3. 測試Ollama連接

```bash
python3 scripts/test_ollama.py
```

## 🧪 測試本地LLM功能

### 1. 啟動系統

```bash
# 啟動Ollama服務 (如果還沒啟動)
ollama serve

# 啟動你的麻醉系統
uvicorn app.main:app --reload
```

### 2. 測試API

```bash
# 測試生成麻醉須知 (使用本地LLM)
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

### 3. 使用Web界面

訪問：http://localhost:8000/docs

## 🔄 切換AI服務

### 使用本地LLM (Ollama)
```bash
export USE_LOCAL_LLM=true
```

### 使用OpenAI
```bash
export USE_LOCAL_LLM=false
export OPENAI_API_KEY=your_api_key_here
```

## 📊 模型比較

| 模型 | 大小 | 記憶體需求 | 中文支援 | 速度 |
|------|------|------------|----------|------|
| qwen2.5:7b | ~4GB | ~8GB RAM | ✅ 優秀 | 中等 |
| qwen2.5:3b | ~2GB | ~4GB RAM | ✅ 良好 | 快速 |
| llama3.1:7b | ~4GB | ~8GB RAM | ❌ 英文 | 中等 |

## 🚨 故障排除

### 問題1: 無法連接到Ollama
```bash
# 檢查Ollama是否運行
curl http://localhost:11434/api/tags

# 重新啟動Ollama
ollama serve
```

### 問題2: 模型未找到
```bash
# 列出已下載的模型
ollama list

# 下載模型
ollama pull qwen2.5:7b
```

### 問題3: 記憶體不足
```bash
# 使用更小的模型
ollama pull qwen2.5:3b
```

## 🎯 使用場景

### 場景1: 完全本地運行
- 設定 `USE_LOCAL_LLM=true`
- 不需要網路連線
- 適合隱私敏感環境

### 場景2: 混合使用
- 本地開發時使用Ollama
- 生產環境使用OpenAI
- 通過環境變數切換

### 場景3: 成本控制
- 使用免費的本地LLM
- 避免OpenAI API費用
- 適合大量測試

## 🔧 進階配置

### 自定義模型參數

在 `app/services/anesthesia_service.py` 中修改：

```python
payload = {
    "model": self.ollama_model,
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.7,    # 創意度 (0-1)
        "top_p": 0.9,         # 核採樣
        "top_k": 40,          # 候選詞數量
        "repeat_penalty": 1.1  # 重複懲罰
    }
}
```

### 使用不同的模型

```bash
# 下載其他模型
ollama pull llama3.1:7b
ollama pull mistral:7b

# 修改 .env 文件
OLLAMA_MODEL=llama3.1:7b
```

## 🎉 完成！

現在你的麻醉須知生成系統完全支援本地LLM了！

- ✅ 可以完全在本地運行
- ✅ 不需要網路連線
- ✅ 不需要API費用
- ✅ 完全控制AI回應

開始享受本地AI的強大功能吧！🚀
