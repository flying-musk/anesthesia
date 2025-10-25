# 醫療多語言功能指南

## 概述

本系統現在支持醫療病史和手術記錄的多語言功能，可以同時生成和存儲英文、中文和法文版本。

## 功能特點

### 1. 多語言數據存儲
- 每個醫療病史和手術記錄都會自動生成三種語言版本
- 使用 `group_id` 來關聯同一組的多語言記錄
- 支持按語言篩選查詢

### 2. API 端點更新

#### 醫療病史 API
- `GET /api/v1/patients/{patient_id}/medical-history?language=en` - 獲取指定語言的醫療病史
- `POST /api/v1/patients/{patient_id}/medical-history` - 創建多語言醫療病史

#### 手術記錄 API
- `GET /api/v1/patients/{patient_id}/surgery-records?language=zh` - 獲取指定語言的手術記錄
- `POST /api/v1/patients/{patient_id}/surgery-records` - 創建多語言手術記錄

### 3. 支持語言
- `en` - 英文
- `zh` - 中文
- `fr` - 法文

## 部署步驟

### 1. 運行數據庫遷移
```bash
cd backend
python3 scripts/migrate_medical_multilingual.py
```

### 2. 初始化多語言樣本數據
```bash
python3 scripts/init_multilingual_sample_data.py
```

### 3. 測試多語言功能
```bash
python3 scripts/test_medical_multilingual.py
```

## API 使用示例

### 創建多語言醫療病史
```bash
curl -X POST "http://localhost:8000/api/v1/patients/1/medical-history" \
  -H "Content-Type: application/json" \
  -d '{
    "allergies": "Penicillin allergy",
    "chronic_conditions": "Hypertension",
    "current_medications": "Lisinopril 10mg daily",
    "previous_surgeries": "Appendectomy in 2000",
    "family_history": "Father had heart disease",
    "other_medical_info": "Regular checkups, stable condition."
  }'
```

### 獲取中文版醫療病史
```bash
curl "http://localhost:8000/api/v1/patients/1/medical-history?language=zh"
```

### 創建多語言手術記錄
```bash
curl -X POST "http://localhost:8000/api/v1/patients/1/surgery-records" \
  -H "Content-Type: application/json" \
  -d '{
    "surgery_name": "Cataract surgery",
    "surgery_type": "regional",
    "surgery_date": "2025-01-15",
    "surgeon_name": "Dr. Michael Chen",
    "anesthesiologist_name": "Dr. Robert Taylor",
    "surgery_duration": 120,
    "anesthesia_duration": 90,
    "pre_surgery_assessment": "Patient assessed for cataract surgery. Vital signs stable.",
    "post_surgery_notes": "Patient recovered well. No complications noted.",
    "complications": "None"
  }'
```

### 獲取法文版手術記錄
```bash
curl "http://localhost:8000/api/v1/patients/1/surgery-records?language=fr"
```

## 數據庫結構

### MedicalHistory 表新增字段
- `language` VARCHAR(10) - 語言版本 (en, zh, fr)
- `group_id` INTEGER - 用於關聯同一組的多語言版本

### SurgeryRecord 表新增字段
- `language` VARCHAR(10) - 語言版本 (en, zh, fr)
- `group_id` INTEGER - 用於關聯同一組的多語言版本

## 翻譯服務

系統使用 `MedicalMultilingualService` 來處理多語言翻譯：

- 英文版本：直接使用原始數據
- 中文和法文版本：使用 AI 翻譯服務（可擴展）

## 故障排除

### 1. 數據庫遷移失敗
```bash
# 檢查數據庫連接
python3 -c "from app.core.database import get_db_engine; print('DB connected')"

# 手動運行遷移
python3 scripts/migrate_medical_multilingual.py
```

### 2. 樣本數據創建失敗
```bash
# 檢查現有數據
python3 -c "
from app.core.database import get_db
from app.models.patient import Patient
db = next(get_db())
print(f'Patients: {db.query(Patient).count()}')
db.close()
"

# 重新創建樣本數據
python3 scripts/init_multilingual_sample_data.py
```

### 3. API 測試
```bash
# 測試醫療病史 API
curl "http://localhost:8000/api/v1/patients/1/medical-history?language=en"

# 測試手術記錄 API
curl "http://localhost:8000/api/v1/patients/1/surgery-records?language=zh"
```

## 注意事項

1. **數據一致性**：所有語言版本都使用相同的 `group_id` 來確保關聯性
2. **翻譯質量**：目前使用模擬翻譯，生產環境需要集成真實的 AI 翻譯服務
3. **性能考慮**：多語言數據會增加存儲空間，建議定期清理不需要的語言版本
4. **API 兼容性**：現有的 API 調用仍然有效，會返回默認語言版本

## 擴展功能

### 添加新語言
1. 在 `LanguageEnum` 中添加新語言
2. 更新 `MedicalMultilingualService` 的翻譯邏輯
3. 運行數據庫遷移腳本

### 集成真實翻譯服務
1. 修改 `_translate_text` 方法
2. 集成 OpenAI、Google Translate 或其他翻譯 API
3. 添加錯誤處理和重試機制
