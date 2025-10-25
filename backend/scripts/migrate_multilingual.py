#!/usr/bin/env python3
"""
Database migration script to add language support to anesthesia guidelines
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.database import Base, engine
from app.models.anesthesia import AnesthesiaGuideline
from app.models.patient import Patient
from loguru import logger

def migrate_database():
    """Add language column to anesthesia_guidelines table"""
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # Check if language column already exists
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM pragma_table_info('anesthesia_guidelines') 
                WHERE name = 'language'
            """))
            
            column_exists = result.fetchone()[0] > 0
            
            if not column_exists:
                logger.info("Adding language column to anesthesia_guidelines table...")
                
                # Add language column with default value 'en'
                conn.execute(text("""
                    ALTER TABLE anesthesia_guidelines 
                    ADD COLUMN language VARCHAR(10) NOT NULL DEFAULT 'en'
                """))
                
                # Create index on language column for better performance
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_anesthesia_guidelines_language 
                    ON anesthesia_guidelines(language)
                """))
                
                conn.commit()
                logger.info("Successfully added language column to anesthesia_guidelines table")
            else:
                logger.info("Language column already exists in anesthesia_guidelines table")
            
            # Check if group_id column exists
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM pragma_table_info('anesthesia_guidelines') 
                WHERE name = 'group_id'
            """))
            
            group_id_exists = result.fetchone()[0] > 0
            
            if not group_id_exists:
                logger.info("Adding group_id column to anesthesia_guidelines table...")
                
                # Add group_id column
                conn.execute(text("""
                    ALTER TABLE anesthesia_guidelines 
                    ADD COLUMN group_id INTEGER
                """))
                
                # Create index on group_id column for better performance
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_anesthesia_guidelines_group_id 
                    ON anesthesia_guidelines(group_id)
                """))
                
                conn.commit()
                logger.info("Successfully added group_id column to anesthesia_guidelines table")
            else:
                logger.info("Group_id column already exists in anesthesia_guidelines table")
                
    except Exception as e:
        logger.error(f"Error during migration: {str(e)}")
        raise

def rollback_migration():
    """Rollback the language column addition"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            logger.info("Rolling back language column from anesthesia_guidelines table...")
            
            # Drop the index first
            conn.execute(text("""
                DROP INDEX IF EXISTS idx_anesthesia_guidelines_language
            """))
            
            # Drop the language column
            conn.execute(text("""
                ALTER TABLE anesthesia_guidelines DROP COLUMN language
            """))
            
            conn.commit()
            logger.info("Successfully rolled back language column from anesthesia_guidelines table")
            
    except Exception as e:
        logger.error(f"Error during rollback: {str(e)}")
        raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration for multilingual support")
    parser.add_argument("--rollback", action="store_true", help="Rollback the migration")
    
    args = parser.parse_args()
    
    if args.rollback:
        rollback_migration()
    else:
        migrate_database()
