#!/usr/bin/env python3
"""
Run date column migration for tech support table
"""
import psycopg2
from config import get_db_connection

def run_migration():
    """Run the date column migration"""
    try:
        # Read the migration file
        with open('migrations/add_date_to_tech_support.sql', 'r') as f:
            migration_sql = f.read()
        
        # Get database connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Execute the migration
        cur.execute(migration_sql)
        conn.commit()
        
        print("✅ Date column migration completed successfully!")
        print("📅 Added issue_date column to tech_support_requests table")
        print("🔄 Updated existing records with created_at date")
        print("✅ Set issue_date as NOT NULL constraint")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    run_migration()
