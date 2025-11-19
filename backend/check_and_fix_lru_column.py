#!/usr/bin/env python3
"""
Check if lru_part_number column exists and add it if it doesn't
"""

from config import get_db_connection

def check_and_fix():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'lrus' AND column_name = 'lru_part_number'
        """)
        result = cur.fetchone()
        
        if result:
            print("✓ Column 'lru_part_number' already exists in 'lrus' table")
            cur.close()
            return True
        else:
            print("✗ Column 'lru_part_number' does NOT exist. Adding it now...")
            
            # Add the column
            cur.execute("""
                ALTER TABLE lrus ADD COLUMN lru_part_number VARCHAR(100)
            """)
            
            # Add comment
            cur.execute("""
                COMMENT ON COLUMN lrus.lru_part_number IS 'LRU Part Number - supports mix of numbers, text, and symbols (e.g., ABC-123-XYZ, 456/789, etc.)'
            """)
            
            conn.commit()
            print("✓ Column 'lru_part_number' added successfully!")
            
            # Verify
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'lrus' AND column_name = 'lru_part_number'
            """)
            verify = cur.fetchone()
            
            if verify:
                print("✓ Verification: Column exists in database")
            else:
                print("✗ Verification failed: Column still not found")
            
            cur.close()
            return True
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
        return False

if __name__ == "__main__":
    print("Checking lru_part_number column...")
    print("=" * 50)
    success = check_and_fix()
    if success:
        print("\n[SUCCESS] Database is ready!")
    else:
        print("\n[ERROR] Failed to fix database")

