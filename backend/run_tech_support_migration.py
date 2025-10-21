#!/usr/bin/env python3
"""
Run tech support table migration
"""
import psycopg2
from config import get_db_connection

def run_migration():
    """Run the tech support table migration"""
    try:
        # Read the migration file
        with open('migrations/create_tech_support_table.sql', 'r') as f:
            migration_sql = f.read()
        
        # Get database connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Execute the migration
        cur.execute(migration_sql)
        conn.commit()
        
        print("✅ Tech support table migration completed successfully!")
        print("📋 Created table: tech_support_requests")
        print("🔑 Primary key: id (SERIAL)")
        print("🔗 Foreign key: user_id references users(user_id)")
        print("📝 Fields: username, user_id, issue_description, status, created_at, updated_at")
        print("📊 Indexes created for performance optimization")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    run_migration()
