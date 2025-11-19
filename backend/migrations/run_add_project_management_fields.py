#!/usr/bin/env python3
"""
Migration script to add project management fields to projects table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_db_connection

def run_migration():
    """Run the migration to add project management fields"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("Starting migration to add project management fields...")
        
        # Check if columns already exist
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'projects' AND column_name IN ('project_director', 'deputy_project_director', 'qa_manager')
        """)
        existing_columns = [row[0] for row in cur.fetchall()]
        
        # Read the SQL file
        migration_file = os.path.join(os.path.dirname(__file__), 'add_project_management_fields.sql')
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Execute the SQL statements one by one
        # First add columns
        try:
            cur.execute("ALTER TABLE projects ADD COLUMN IF NOT EXISTS project_director VARCHAR(100)")
            print("✓ Added project_director column")
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"Error adding project_director: {str(e)}")
                raise
        
        try:
            cur.execute("ALTER TABLE projects ADD COLUMN IF NOT EXISTS deputy_project_director VARCHAR(100)")
            print("✓ Added deputy_project_director column")
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"Error adding deputy_project_director: {str(e)}")
                raise
        
        try:
            cur.execute("ALTER TABLE projects ADD COLUMN IF NOT EXISTS qa_manager VARCHAR(100)")
            print("✓ Added qa_manager column")
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"Error adding qa_manager: {str(e)}")
                raise
        
        # Then add comments
        try:
            cur.execute("COMMENT ON COLUMN projects.project_director IS 'Project Director name - supports text with spaces'")
            print("✓ Added comment for project_director")
        except Exception as e:
            print(f"Warning: Could not add comment for project_director: {str(e)}")
        
        try:
            cur.execute("COMMENT ON COLUMN projects.deputy_project_director IS 'Deputy Project Director name - supports text with spaces'")
            print("✓ Added comment for deputy_project_director")
        except Exception as e:
            print(f"Warning: Could not add comment for deputy_project_director: {str(e)}")
        
        try:
            cur.execute("COMMENT ON COLUMN projects.qa_manager IS 'QA Manager name - supports text with spaces'")
            print("✓ Added comment for qa_manager")
        except Exception as e:
            print(f"Warning: Could not add comment for qa_manager: {str(e)}")
        
        # Commit changes
        conn.commit()
        print("\nMigration completed successfully!")
        
        # Verify columns were added
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'projects' AND column_name IN ('project_director', 'deputy_project_director', 'qa_manager')
        """)
        verify_columns = [row[0] for row in cur.fetchall()]
        
        print(f"\nColumn verification:")
        for col in ['project_director', 'deputy_project_director', 'qa_manager']:
            exists = col in verify_columns
            print(f"  - {col}: {'✓' if exists else '✗'}")
        
        cur.close()
        return True
        
    except Exception as e:
        print(f"\nMigration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
        return False

if __name__ == "__main__":
    print("Add Project Management Fields Migration")
    print("=" * 50)
    success = run_migration()
    
    if success:
        print("\n[SUCCESS] Migration completed successfully!")
    else:
        print("\n[ERROR] Migration failed. Please check the error messages above.")
        sys.exit(1)

