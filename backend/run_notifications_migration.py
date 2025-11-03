#!/usr/bin/env python3
"""
Run notifications migration to add notification support to activity_logs table
"""
import psycopg2
from config import get_db_connection

def run_migration():
    """Run the notifications migration"""
    try:
        # Read the migration file
        with open('migrations/add_notifications_to_activity_logs.sql', 'r') as f:
            migration_sql = f.read()
        
        # Get database connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Execute the migration
        cur.execute(migration_sql)
        conn.commit()
        
        print("✅ Notifications migration completed successfully!")
        print("📊 Added notified_user_id column (FK to users table)")
        print("📝 Added is_read boolean column")
        print("🏷️ Added notification_type VARCHAR column")
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

