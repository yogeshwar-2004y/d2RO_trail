#!/usr/bin/env python3
"""
Migration script to add lru_part_number column to lrus table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_db_connection

def run_migration():
    """Run the migration to add lru_part_number column to lrus table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("Starting migration to add lru_part_number column to lrus table...")
        
        # Check if column already exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'lrus' AND column_name = 'lru_part_number'
            );
        """)
        column_exists = cur.fetchone()[0]
        
        if column_exists:
            print("Column 'lru_part_number' already exists. Migration not needed.")
            cur.close()
            return True
        
        # Read the SQL file
        migration_file = os.path.join(os.path.dirname(__file__), 'add_lru_part_number_to_lrus.sql')
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Execute the SQL (split by semicolons to handle multiple statements)
        statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for statement in statements:
            if statement:
                try:
                    cur.execute(statement)
                    print(f"Executed: {statement[:80]}...")
                except Exception as e:
                    print(f"Error executing statement: {str(e)}")
                    raise
        
        # Commit changes
        conn.commit()
        print("\nMigration completed successfully!")
        
        # Verify column was added
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'lrus' AND column_name = 'lru_part_number'
            );
        """)
        column_exists = cur.fetchone()[0]
        
        if column_exists:
            # Get column details
            cur.execute("""
                SELECT data_type, character_maximum_length, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'lrus' AND column_name = 'lru_part_number'
            """)
            col_info = cur.fetchone()
            print(f"\nColumn verification:")
            print(f"  - Column exists: {column_exists}")
            print(f"  - Data type: {col_info[0]}")
            print(f"  - Max length: {col_info[1]}")
            print(f"  - Nullable: {col_info[2]}")
        
        cur.close()
        return True
        
    except Exception as e:
        print(f"\nMigration failed: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
        return False

if __name__ == "__main__":
    print("Add LRU Part Number Column Migration")
    print("=" * 50)
    
    success = run_migration()
    
    if success:
        print("\n[SUCCESS] Migration completed successfully!")
    else:
        print("\n[ERROR] Migration failed. Please check the error messages above.")
        sys.exit(1)

