# 🏥 麻醉前須知生成系統

基於AI的個人化麻醉前須知生成系統，支援多語言界面（中文、英文、法文）。

## 📁 專案結構

```
anesthesia-backend/
├── frontend/                 # React前端應用
│   ├── public/              # 靜態資源
│   ├── src/
│   │   ├── components/      # React組件
│   │   ├── pages/           # 頁面組件
│   │   ├── services/        # API服務
│   │   ├── i18n/           # 國際化配置
│   │   └── ...
│   ├── package.json
│   └── ...
├── backend/                 # FastAPI後端
│   ├── app/                # 應用程式代碼
│   ├── scripts/            # 腳本文件
│   ├── requirements.txt
│   └── ...
├── README.md
└── ...
```

## 🚀 快速開始

### 1. 啟動後端服務

```bash
cd backend
pip install -r requirements.txt
python start_demo.py
uvicorn app.main:app --reload
```

### 2. 啟動前端服務

```bash
cd frontend
npm install
npm start
```

### 3. 訪問系統

- **前端界面**: http://localhost:3000
- **API文檔**: http://localhost:8000/docs
- **健康檢查**: http://localhost:8000/health

## 🌍 多語言支援

系統支援三種語言：
- 🇹🇼 繁體中文 (zh-TW)
- 🇺🇸 English (en-US)
- 🇫🇷 Français (fr-FR)

用戶可以在界面右上角切換語言。

## 🎯 主要功能

### 前端功能
- ✅ 多語言界面支援
- ✅ 患者管理（新增、搜尋、查看、編輯）
- ✅ 麻醉須知生成
- ✅ 響應式設計
- ✅ 現代化UI界面

### 後端功能
- ✅ RESTful API
- ✅ 患者管理系統
- ✅ 醫療病史管理
- ✅ AI麻醉須知生成
- ✅ 本地LLM支援 (Ollama)
- ✅ OpenAI API整合

## 🛠️ 技術棧

### 前端
- React 18
- Material-UI (MUI)
- React Router
- React Query
- React Hook Form
- i18next (國際化)
- Axios

### 後端
- FastAPI
- SQLAlchemy
- SQLite
- OpenAI API
- Ollama (本地LLM)
- Pydantic

## 📋 API端點

### 患者管理
- `GET /api/v1/patients/` - 獲取所有患者
- `POST /api/v1/patients/` - 創建患者
- `GET /api/v1/patients/{id}` - 獲取患者詳情
- `PUT /api/v1/patients/{id}` - 更新患者
- `DELETE /api/v1/patients/{id}` - 刪除患者
- `POST /api/v1/patients/search` - 搜尋患者

### 麻醉須知
- `POST /api/v1/anesthesia/guidelines/generate` - 生成麻醉須知
- `GET /api/v1/anesthesia/guidelines/` - 獲取所有麻醉須知
- `GET /api/v1/anesthesia/guidelines/{id}` - 獲取麻醉須知詳情
- `PUT /api/v1/anesthesia/guidelines/{id}` - 更新麻醉須知
- `DELETE /api/v1/anesthesia/guidelines/{id}` - 刪除麻醉須知

## 🔧 配置

### 環境變數

創建 `.env` 文件：

```bash
# 使用本地LLM (Ollama)
USE_LOCAL_LLM=true
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# 或使用OpenAI
OPENAI_API_KEY=your_api_key_here
USE_LOCAL_LLM=false

# 其他設定
DEBUG=true
DATABASE_URL=sqlite:///./anesthesia.db
```

### 本地LLM設定

1. 安裝Ollama
2. 下載模型：`ollama pull qwen2.5:7b`
3. 啟動服務：`ollama serve`
4. 設定環境變數：`USE_LOCAL_LLM=true`

## 🧪 測試

### 後端測試
```bash
cd backend
python scripts/test_api.py
```

### 前端測試
```bash
cd frontend
npm test
```

## 📚 文檔

- [快速開始指南](backend/QUICK_START.md)
- [本地LLM設定指南](backend/LOCAL_LLM_GUIDE.md)
- [API文檔](http://localhost:8000/docs)

## 🤝 貢獻

歡迎提交Issue和Pull Request！

## 📄 授權

MIT License

---

🎉 **系統已準備就緒！** 現在你可以開始使用這個強大的麻醉前須知生成系統了！