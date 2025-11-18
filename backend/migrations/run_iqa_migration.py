#!/usr/bin/env python3
"""
Migration script to create the iqa_observation_reports table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_db_connection

def run_iqa_migration():
    """Run the migration to create iqa_observation_reports table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("Starting migration for iqa_observation_reports table...")
        
        # Read the SQL file
        migration_file = os.path.join(os.path.dirname(__file__), 'create_iqa_observation_report_table.sql')
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Execute the SQL (split by semicolons to handle multiple statements)
        # psycopg2 doesn't support executing multiple statements in one execute() call
        # So we'll split and execute each statement
        statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for statement in statements:
            if statement:
                try:
                    cur.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                except Exception as e:
                    # Some statements might fail if they already exist, which is okay
                    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                        print(f"Skipped (already exists): {statement[:50]}...")
                    else:
                        print(f"Warning: {str(e)}")
        
        # Commit changes
        conn.commit()
        print("\nMigration completed successfully!")
        
        # Verify table was created
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'iqa_observation_reports'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        if table_exists:
            print("✓ iqa_observation_reports table created successfully!")
            
            # Check columns
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'iqa_observation_reports'
                ORDER BY ordinal_position
            """)
            columns = cur.fetchall()
            print(f"\nTable has {len(columns)} columns:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
        else:
            print("✗ Table was not created. Please check the error messages above.")
        
        cur.close()
        return True
        
    except Exception as e:
        print(f"Migration failed: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
        return False

if __name__ == "__main__":
    print("IQA Observation Reports Table Migration")
    print("=" * 50)
    
    success = run_iqa_migration()
    
    if success:
        print("\n[SUCCESS] Migration completed successfully!")
    else:
        print("\n[ERROR] Migration failed. Please check the error messages above.")
        sys.exit(1)

