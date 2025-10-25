#!/usr/bin/env python3
"""
醫療病史和手術記錄多語言遷移腳本
為 medical_histories 和 surgery_records 表添加 language 和 group_id 字段
"""

import os
import sys
from sqlalchemy import create_engine, text

# Add the parent directory to the Python path to allow imports from 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.core.config import settings
from app.core.database import engine

def migrate_medical_multilingual():
    """為醫療病史和手術記錄添加多語言支持"""
    
    with engine.connect() as conn:
        # 開始事務
        trans = conn.begin()
        try:
            print("=== 開始醫療多語言遷移 ===")
            
            # 為 medical_histories 表添加 language 字段
            print("1. 為 medical_histories 表添加 language 字段...")
            conn.execute(text("""
                ALTER TABLE medical_histories
                ADD COLUMN language VARCHAR(10) NOT NULL DEFAULT 'en'
            """))
            
            # 為 medical_histories 表添加 group_id 字段
            print("2. 為 medical_histories 表添加 group_id 字段...")
            conn.execute(text("""
                ALTER TABLE medical_histories
                ADD COLUMN group_id INTEGER
            """))
            
            # 為 medical_histories 表創建索引
            print("3. 為 medical_histories 表創建索引...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_medical_histories_language
                ON medical_histories(language)
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_medical_histories_group_id
                ON medical_histories(group_id)
            """))
            
            # 為 surgery_records 表添加 language 字段
            print("4. 為 surgery_records 表添加 language 字段...")
            conn.execute(text("""
                ALTER TABLE surgery_records
                ADD COLUMN language VARCHAR(10) NOT NULL DEFAULT 'en'
            """))
            
            # 為 surgery_records 表添加 group_id 字段
            print("5. 為 surgery_records 表添加 group_id 字段...")
            conn.execute(text("""
                ALTER TABLE surgery_records
                ADD COLUMN group_id INTEGER
            """))
            
            # 為 surgery_records 表創建索引
            print("6. 為 surgery_records 表創建索引...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_surgery_records_language
                ON surgery_records(language)
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_surgery_records_group_id
                ON surgery_records(group_id)
            """))
            
            # 提交事務
            trans.commit()
            print("✅ 醫療多語言遷移完成！")
            
        except Exception as e:
            # 回滾事務
            trans.rollback()
            print(f"❌ 遷移失敗: {e}")
            raise

if __name__ == "__main__":
    migrate_medical_multilingual()
