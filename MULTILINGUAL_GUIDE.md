# 多語言麻醉須知系統使用指南

## 概述

本系統現在支持生成英文、中文和法文三種語言版本的麻醉須知。每次生成guideline時，系統會同時創建三種語言版本並存儲在數據庫中。

## 主要功能

### 1. 多語言生成
- 支持英文 (en)、中文 (zh)、法文 (fr) 三種語言
- 每次生成時會同時創建所有語言版本
- 每種語言版本都是獨立的數據庫記錄

### 2. 語言過濾
- API支持按語言過濾查詢結果
- 前端可以選擇顯示特定語言的guideline

## 數據庫變更

### 新增字段
- `anesthesia_guidelines` 表新增 `language` 字段
- 默認值為 'en' (英文)
- 支持 'en', 'zh', 'fr' 三種值

### 遷移腳本
```bash
# 執行遷移
python backend/scripts/migrate_multilingual.py

# 回滾遷移（如果需要）
python backend/scripts/migrate_multilingual.py --rollback
```

## API 變更

### 1. 生成Guideline
**Endpoint:** `POST /api/v1/anesthesia/guidelines/generate`

**重要：系統會固定生成三種語言版本（en, zh, fr）並存儲到數據庫中**

**請求格式:**
```json
{
  "patient_id": 1,
  "surgery_name": "闌尾切除術",
  "anesthesia_type": "general",
  "surgery_date": "2024-01-15",
  "surgeon_name": "張醫師",
  "anesthesiologist_name": "李麻醉師",
  "return_language": "zh"  // 可選，指定要回傳的語言版本
}
```

**回應格式（指定語言時）:**
```json
{
  "id": 2,
  "patient_id": 1,
  "language": "zh",
  "surgery_name": "闌尾切除術",
  "anesthesia_type_info": "全身麻醉的中文說明...",
  // ... 其他字段
}
```

**回應格式（不指定語言時，回傳所有語言）:**
```json
[
  {
    "id": 1,
    "patient_id": 1,
    "language": "en",
    "surgery_name": "Appendectomy",
    "anesthesia_type_info": "General anesthesia explanation in English...",
    // ... 其他字段
  },
  {
    "id": 2,
    "patient_id": 1,
    "language": "zh",
    "surgery_name": "闌尾切除術",
    "anesthesia_type_info": "全身麻醉的中文說明...",
    // ... 其他字段
  },
  {
    "id": 3,
    "patient_id": 1,
    "language": "fr",
    "surgery_name": "Appendicectomie",
    "anesthesia_type_info": "Explication de l'anesthésie générale en français...",
    // ... 其他字段
  }
]
```

### 2. 查詢Guideline
**Endpoint:** `GET /api/v1/anesthesia/guidelines`

**查詢參數:**
- `language`: 可選，過濾特定語言 (en, zh, fr)
- `page`, `size`: 分頁參數

**範例:**
```
GET /api/v1/anesthesia/guidelines?language=zh&page=1&size=10
```

### 3. 獲取特定Guideline
**Endpoint:** `GET /api/v1/anesthesia/guidelines/{guideline_id}`

**查詢參數:**
- `language`: 可選，返回同一組的特定語言版本

**重要說明:**
- 系統使用 `group_id` 來關聯同一組的多語言版本
- 當你指定 `language` 參數時，系統會找到具有相同 `group_id` 的對應語言版本
- 例如：如果你有ID=16的中文版本，查詢 `?language=fr` 會返回同一組的法文版本（可能是ID=17或18）

**範例:**
```
GET /api/v1/anesthesia/guidelines/16?language=fr
```

### 4. 獲取患者Guideline
**Endpoint:** `GET /api/v1/anesthesia/guidelines/patient/{patient_id}`

**查詢參數:**
- `language`: 可選，過濾特定語言

**範例:**
```
GET /api/v1/anesthesia/guidelines/patient/1?language=zh
```

## 前端集成

### 1. 語言選擇
前端可以添加語言選擇器：
```javascript
const languageOptions = [
  { value: 'en', label: 'English' },
  { value: 'zh', label: '中文' },
  { value: 'fr', label: 'Français' }
];
```

### 2. API調用範例
```javascript
// 生成guideline（固定生成三種語言，但只回傳中文版本）
const generateGuideline = async (patientData) => {
  const response = await fetch('/api/v1/anesthesia/guidelines/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...patientData,
      return_language: 'zh'  // 只回傳中文版本
    })
  });
  return response.json();
};

// 生成guideline（回傳所有語言版本）
const generateAllLanguages = async (patientData) => {
  const response = await fetch('/api/v1/anesthesia/guidelines/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...patientData
      // 不指定 return_language，會回傳所有語言
    })
  });
  return response.json();
};

// 獲取特定語言的guideline
const getGuidelineByLanguage = async (guidelineId, language) => {
  const response = await fetch(
    `/api/v1/anesthesia/guidelines/${guidelineId}?language=${language}`
  );
  return response.json();
};
```

## 測試

### 運行測試腳本
```bash
# 測試多語言生成
python backend/scripts/test_multilingual.py

# 測試單語言生成
python backend/scripts/test_multilingual.py --single
```

## 部署步驟

1. **執行數據庫遷移**:
   ```bash
   # 添加語言支持
   python backend/scripts/migrate_multilingual.py
   
   # 添加group_id支持
   python backend/scripts/migrate_group_id.py
   ```

2. **測試功能**:
   ```bash
   python backend/scripts/test_multilingual.py
   ```

3. **更新前端**: 根據 `MULTILINGUAL_GUIDE.md` 中的說明更新前端代碼

## 配置

### 環境變量
確保以下環境變量已正確設置：
- `OPENAI_API_KEY`: OpenAI API密鑰
- `USE_LOCAL_LLM`: 是否使用本地LLM (true/false)
- `OLLAMA_URL`: Ollama服務URL (如果使用本地LLM)
- `OLLAMA_MODEL`: Ollama模型名稱 (如果使用本地LLM)

## 注意事項

1. **數據庫遷移**: 在部署前務必執行遷移腳本
2. **性能考慮**: 多語言生成會增加API響應時間
3. **存儲空間**: 每條guideline會生成3個語言版本，需要更多存儲空間
4. **AI成本**: 使用OpenAI時，多語言生成會增加API調用成本

## 故障排除

### 常見問題

1. **遷移失敗**: 檢查數據庫連接和權限
2. **生成失敗**: 檢查AI服務配置和網絡連接
3. **語言過濾不工作**: 檢查API參數格式

### 日誌查看
```bash
# 查看應用日誌
tail -f logs/app.log

# 查看錯誤日誌
tail -f logs/error.log
```
