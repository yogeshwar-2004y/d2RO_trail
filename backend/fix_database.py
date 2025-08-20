#!/usr/bin/env python3
"""
Script to fix database schema for password hashing
"""

import psycopg2

def fix_database_schema():
    """Fix the password_hash column to accommodate SHA-256 hashes"""
    try:
        # Connect to database
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(
            dbname="ERP",
            user="postgres",
            password="Admin",
            host="localhost",
            port="5432"
        )
        
        cur = conn.cursor()
        print("✅ Database connected!")
        
        # Check current column definition
        print("\n🔍 Checking current password_hash column definition...")
        cur.execute("""
            SELECT column_name, data_type, character_maximum_length 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'password_hash'
        """)
        
        column_info = cur.fetchone()
        if column_info:
            print(f"  Column: {column_info[0]}")
            print(f"  Type: {column_info[1]}")
            print(f"  Max Length: {column_info[2]}")
        
        # Alter the column to accommodate SHA-256 hashes (64 characters)
        print("\n🔄 Altering password_hash column...")
        cur.execute("ALTER TABLE users ALTER COLUMN password_hash TYPE VARCHAR(64)")
        
        conn.commit()
        print("✅ Column altered successfully!")
        
        # Verify the change
        print("\n🔍 Verifying column change...")
        cur.execute("""
            SELECT column_name, data_type, character_maximum_length 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'password_hash'
        """)
        
        column_info = cur.fetchone()
        if column_info:
            print(f"  Column: {column_info[0]}")
            print(f"  Type: {column_info[1]}")
            print(f"  Max Length: {column_info[2]}")
        
        cur.close()
        conn.close()
        print("\n✅ Database schema fixed!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_database_schema()
