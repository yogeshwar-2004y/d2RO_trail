#!/usr/bin/env python3
"""
Check current database state and apply migration safely
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_db_connection

def check_current_state():
    """Check the current state of the database tables"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("Checking current database state...")
        
        # Check if tables exist
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'document_comments'
            );
        """)
        comments_exists = cur.fetchone()[0]
        
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'document_annotations'
            );
        """)
        annotations_exists = cur.fetchone()[0]
        
        print(f"document_comments exists: {comments_exists}")
        print(f"document_annotations exists: {annotations_exists}")
        
        if comments_exists:
            # Check current schema
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'document_comments' AND column_name = 'document_id'
            """)
            comments_schema = cur.fetchone()
            print(f"document_comments.document_id type: {comments_schema}")
            
            # Check record count
            cur.execute("SELECT COUNT(*) FROM document_comments")
            comments_count = cur.fetchone()[0]
            print(f"document_comments record count: {comments_count}")
            
            # Check sample data
            cur.execute("SELECT document_id, document_name FROM document_comments LIMIT 3")
            sample_data = cur.fetchall()
            print(f"Sample document_comments data: {sample_data}")
        
        if annotations_exists:
            # Check current schema
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'document_annotations' AND column_name = 'document_id'
            """)
            annotations_schema = cur.fetchone()
            print(f"document_annotations.document_id type: {annotations_schema}")
            
            # Check record count
            cur.execute("SELECT COUNT(*) FROM document_annotations")
            annotations_count = cur.fetchone()[0]
            print(f"document_annotations record count: {annotations_count}")
        
        cur.close()
        return comments_exists, annotations_exists
        
    except Exception as e:
        print(f"Error checking database state: {e}")
        return False, False

def apply_safe_migration():
    """Apply migration safely by altering existing tables"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("\nApplying safe migration by altering existing tables...")
        
        # Step 1: Create backup tables
        print("Creating backup tables...")
        cur.execute("DROP TABLE IF EXISTS document_comments_backup")
        cur.execute("CREATE TABLE document_comments_backup AS SELECT * FROM document_comments")
        
        cur.execute("DROP TABLE IF EXISTS document_annotations_backup")
        cur.execute("CREATE TABLE document_annotations_backup AS SELECT * FROM document_annotations")
        
        # Step 2: Add new integer columns
        print("Adding new integer document_id columns...")
        cur.execute("ALTER TABLE document_comments ADD COLUMN document_id_new INT")
        cur.execute("ALTER TABLE document_annotations ADD COLUMN document_id_new INT")
        
        # Step 3: Populate new columns with actual document_id from plan_documents
        print("Populating new columns with actual document_id...")
        cur.execute("""
            UPDATE document_comments 
            SET document_id_new = pd.document_id
            FROM plan_documents pd 
            WHERE document_comments.document_id = pd.document_number
        """)
        
        cur.execute("""
            UPDATE document_annotations 
            SET document_id_new = pd.document_id
            FROM plan_documents pd 
            WHERE document_annotations.document_id = pd.document_number
        """)
        
        # Step 4: Drop old columns and rename new ones
        print("Replacing old columns with new ones...")
        cur.execute("ALTER TABLE document_comments DROP COLUMN document_id")
        cur.execute("ALTER TABLE document_annotations DROP COLUMN document_id")
        
        cur.execute("ALTER TABLE document_comments RENAME COLUMN document_id_new TO document_id")
        cur.execute("ALTER TABLE document_annotations RENAME COLUMN document_id_new TO document_id")
        
        # Step 5: Add foreign key constraints
        print("Adding foreign key constraints...")
        cur.execute("""
            ALTER TABLE document_comments 
            ADD CONSTRAINT fk_document_comments_document_id 
            FOREIGN KEY (document_id) REFERENCES plan_documents(document_id) ON DELETE CASCADE
        """)
        
        cur.execute("""
            ALTER TABLE document_annotations 
            ADD CONSTRAINT fk_document_annotations_document_id 
            FOREIGN KEY (document_id) REFERENCES plan_documents(document_id) ON DELETE CASCADE
        """)
        
        # Step 6: Add NOT NULL constraints
        print("Adding NOT NULL constraints...")
        cur.execute("ALTER TABLE document_comments ALTER COLUMN document_id SET NOT NULL")
        cur.execute("ALTER TABLE document_annotations ALTER COLUMN document_id SET NOT NULL")
        
        # Step 7: Create indexes
        print("Creating indexes...")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_comments_document_id ON document_comments(document_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_annotations_document_id ON document_annotations(document_id)")
        
        conn.commit()
        print("Migration completed successfully!")
        
        # Verify the migration
        cur.execute("SELECT COUNT(*) FROM document_comments")
        comments_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM document_annotations")
        annotations_count = cur.fetchone()[0]
        
        print(f"Final counts - Comments: {comments_count}, Annotations: {annotations_count}")
        
        cur.close()
        return True
        
    except Exception as e:
        print(f"Migration failed: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False

if __name__ == "__main__":
    print("Database Schema Migration Tool")
    print("=" * 40)
    
    # Check current state
    comments_exists, annotations_exists = check_current_state()
    
    if comments_exists and annotations_exists:
        # Apply safe migration
        success = apply_safe_migration()
        
        if success:
            print("\n[SUCCESS] Migration completed successfully!")
            print("The document_comments and document_annotations tables now:")
            print("- Use INTEGER document_id instead of VARCHAR")
            print("- Have proper foreign key relationships to plan_documents")
            print("- Include proper constraints and indexes")
        else:
            print("\n[ERROR] Migration failed. Please check the error messages above.")
    else:
        print("Tables don't exist. Creating them with correct schema...")
        from utils.database_init import create_comments_tables
        create_comments_tables()
        print("Tables created successfully with correct schema.")
