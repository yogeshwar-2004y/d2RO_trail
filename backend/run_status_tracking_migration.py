#!/usr/bin/env python3
"""
Run status tracking migration for tech support table
"""
import psycopg2
from config import get_db_connection

def run_migration():
    """Run the status tracking migration"""
    try:
        # Read the migration file
        with open('migrations/add_status_tracking_to_tech_support.sql', 'r') as f:
            migration_sql = f.read()
        
        # Get database connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Execute the migration
        cur.execute(migration_sql)
        conn.commit()
        
        print("✅ Status tracking migration completed successfully!")
        print("📊 Added status_updated_by column (FK to users table)")
        print("📅 Added status_updated_at timestamp column")
        print("🔗 Added foreign key constraint")
        print("📈 Created performance indexes")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    run_migration()
