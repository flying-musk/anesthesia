#!/usr/bin/env python3
"""
Database migration script to add group_id support to anesthesia guidelines
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
    """Add group_id column to anesthesia_guidelines table"""
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # Check if group_id column already exists
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM pragma_table_info('anesthesia_guidelines') 
                WHERE name = 'group_id'
            """))
            
            column_exists = result.fetchone()[0] > 0
            
            if not column_exists:
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
    """Rollback the group_id column addition"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            logger.info("Rolling back group_id column from anesthesia_guidelines table...")
            
            # Drop the index first
            conn.execute(text("""
                DROP INDEX IF EXISTS idx_anesthesia_guidelines_group_id
            """))
            
            # Drop the group_id column
            conn.execute(text("""
                ALTER TABLE anesthesia_guidelines DROP COLUMN group_id
            """))
            
            conn.commit()
            logger.info("Successfully rolled back group_id column from anesthesia_guidelines table")
            
    except Exception as e:
        logger.error(f"Error during rollback: {str(e)}")
        raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration for group_id support")
    parser.add_argument("--rollback", action="store_true", help="Rollback the migration")
    
    args = parser.parse_args()
    
    if args.rollback:
        rollback_migration()
    else:
        migrate_database()
