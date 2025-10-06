#!/usr/bin/env python3
"""
Script to run database migrations
"""
import psycopg2
from config import get_db_connection

def run_migration():
    """Run the template_id migration"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Read and execute the migration file
        with open('migrations/add_template_id_to_reports.sql', 'r') as f:
            migration_sql = f.read()
        
        # Execute the migration
        cur.execute(migration_sql)
        conn.commit()
        
        print("✅ Migration completed successfully!")
        print("Added template_id field to reports table")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    run_migration()
