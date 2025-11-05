#!/usr/bin/env python3
"""
Script to run database migration for adding report_card_id to inspection report tables
This migration:
1. Adds report_card_id column to conformal_coating_inspection_report
2. Adds report_card_id column to kit_of_parts_inspection_report
3. Migrates existing data from original_report_id to report_card_id
4. Creates indexes for better query performance
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_db_connection

def run_migration():
    """Run the report_card_id migration"""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Read and execute the migration file
        migration_file_path = os.path.join(os.path.dirname(__file__), 'migrations', 'add_report_card_id_to_inspection_reports.sql')
        
        with open(migration_file_path, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        print("Running migration: Add report_card_id to inspection report tables...")
        print("=" * 60)
        
        # Execute the migration
        cur.execute(migration_sql)
        conn.commit()
        
        print("=" * 60)
        print("✅ Migration completed successfully!")
        print("Added report_card_id field to:")
        print("  - conformal_coating_inspection_report")
        print("  - kit_of_parts_inspection_report")
        print("\n✅ Created indexes for better query performance")
        print("✅ Migrated existing data from original_report_id to report_card_id")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()
        sys.exit(1)

if __name__ == "__main__":
    run_migration()

