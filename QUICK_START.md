# 🚀 快速啟動指南 (Hackathon Demo)

## 一鍵啟動 (推薦)

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 初始化 SQLite 資料庫和 demo 資料
python start_demo.py

# 3. 啟動伺服器
uvicorn app.main:app --reload
```

## 訪問系統

- **API 文檔**: http://localhost:8000/docs
- **ReDoc 文檔**: http://localhost:8000/redoc
- **健康檢查**: http://localhost:8000/health

## Demo 資料

系統會自動建立以下 demo 資料：

### 患者 1: 王小明
- 健保號: `1234567890`
- 姓名: `王小明`
- 生日: `1985-05-15`
- 性別: 男性
- 醫療病史: 青黴素過敏、高血壓

### 患者 2: 李小華
- 健保號: `0987654321`
- 姓名: `李小華`
- 生日: `1990-08-22`
- 性別: 女性
- 醫療病史: 無特殊病史

## 測試 API

### 1. 搜尋患者
```bash
curl -X POST "http://localhost:8000/api/v1/patients/search" \
  -H "Content-Type: application/json" \
  -d '{
    "health_insurance_number": "1234567890",
    "full_name": "王小明",
    "date_of_birth": "1985-05-15"
  }'
```

### 2. 生成麻醉須知
```bash
curl -X POST "http://localhost:8000/api/v1/anesthesia/guidelines/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "surgery_name": "腹腔鏡膽囊切除術",
    "anesthesia_type": "general",
    "surgery_date": "2024-01-15",
    "surgeon_name": "李醫師",
    "anesthesiologist_name": "陳醫師"
  }'
```

### 3. 自動測試
```bash
python scripts/test_api.py
```

## 系統特色

✅ **零配置**: 使用 SQLite，無需安裝資料庫  
✅ **快速啟動**: 一鍵初始化 demo 資料  
✅ **自動文檔**: 自動生成 API 文檔  
✅ **AI 整合**: 使用 OpenAI GPT-4 生成個人化須知  
✅ **完整功能**: 患者管理、醫療病史、麻醉須知生成  

## 故障排除

### 如果遇到 OpenAI API 錯誤
1. 設定環境變數: `export OPENAI_API_KEY=your_api_key_here`
2. 或建立 `.env` 檔案並設定 `OPENAI_API_KEY=your_api_key_here`

### 如果遇到端口被占用
```bash
# 使用不同端口
uvicorn app.main:app --reload --port 8001
```

## 生產環境部署

如需部署到生產環境，建議：
1. 使用 PostgreSQL 替代 SQLite
2. 設定環境變數
3. 使用 Gunicorn 或 Uvicorn 作為 WSGI 伺服器

---

🎯 **Hackathon 準備完成！** 現在你可以專注於前端開發和系統整合了！
