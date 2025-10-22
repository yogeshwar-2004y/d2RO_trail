#!/usr/bin/env python3
"""
Safe migration that handles orphaned records
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_db_connection

def apply_migration_with_cleanup():
    """Apply migration with cleanup of orphaned records"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("Applying migration with orphaned record cleanup...")
        
        # Step 1: Create backup tables
        print("Creating backup tables...")
        cur.execute("DROP TABLE IF EXISTS document_comments_backup")
        cur.execute("CREATE TABLE document_comments_backup AS SELECT * FROM document_comments")
        
        cur.execute("DROP TABLE IF EXISTS document_annotations_backup")
        cur.execute("CREATE TABLE document_annotations_backup AS SELECT * FROM document_annotations")
        
        # Step 2: Check for orphaned records
        print("Checking for orphaned records...")
        cur.execute("""
            SELECT DISTINCT dc.document_id 
            FROM document_comments dc 
            LEFT JOIN plan_documents pd ON dc.document_id = pd.document_number
            WHERE pd.document_id IS NULL
        """)
        orphaned_comments = cur.fetchall()
        print(f"Found {len(orphaned_comments)} orphaned comment document_ids: {orphaned_comments}")
        
        cur.execute("""
            SELECT DISTINCT da.document_id 
            FROM document_annotations da 
            LEFT JOIN plan_documents pd ON da.document_id = pd.document_number
            WHERE pd.document_id IS NULL
        """)
        orphaned_annotations = cur.fetchall()
        print(f"Found {len(orphaned_annotations)} orphaned annotation document_ids: {orphaned_annotations}")
        
        # Step 3: Delete orphaned records
        if orphaned_comments:
            print("Deleting orphaned comment records...")
            for orphaned in orphaned_comments:
                cur.execute("DELETE FROM document_comments WHERE document_id = %s", orphaned)
                print(f"Deleted comments for document_id: {orphaned[0]}")
        
        if orphaned_annotations:
            print("Deleting orphaned annotation records...")
            for orphaned in orphaned_annotations:
                cur.execute("DELETE FROM document_annotations WHERE document_id = %s", orphaned)
                print(f"Deleted annotations for document_id: {orphaned[0]}")
        
        # Step 4: Add new integer columns
        print("Adding new integer document_id columns...")
        cur.execute("ALTER TABLE document_comments ADD COLUMN document_id_new INT")
        cur.execute("ALTER TABLE document_annotations ADD COLUMN document_id_new INT")
        
        # Step 5: Populate new columns with actual document_id from plan_documents
        print("Populating new columns with actual document_id...")
        cur.execute("""
            UPDATE document_comments 
            SET document_id_new = pd.document_id
            FROM plan_documents pd 
            WHERE document_comments.document_id = pd.document_number
        """)
        comments_updated = cur.rowcount
        print(f"Updated {comments_updated} comment records")
        
        cur.execute("""
            UPDATE document_annotations 
            SET document_id_new = pd.document_id
            FROM plan_documents pd 
            WHERE document_annotations.document_id = pd.document_number
        """)
        annotations_updated = cur.rowcount
        print(f"Updated {annotations_updated} annotation records")
        
        # Step 6: Drop old columns and rename new ones
        print("Replacing old columns with new ones...")
        cur.execute("ALTER TABLE document_comments DROP COLUMN document_id")
        cur.execute("ALTER TABLE document_annotations DROP COLUMN document_id")
        
        cur.execute("ALTER TABLE document_comments RENAME COLUMN document_id_new TO document_id")
        cur.execute("ALTER TABLE document_annotations RENAME COLUMN document_id_new TO document_id")
        
        # Step 7: Add foreign key constraints
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
        
        # Step 8: Add NOT NULL constraints
        print("Adding NOT NULL constraints...")
        cur.execute("ALTER TABLE document_comments ALTER COLUMN document_id SET NOT NULL")
        cur.execute("ALTER TABLE document_annotations ALTER COLUMN document_id SET NOT NULL")
        
        # Step 9: Create indexes
        print("Creating indexes...")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_comments_document_id ON document_comments(document_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_annotations_document_id ON document_annotations(document_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_comments_status ON document_comments(status)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_comments_created_at ON document_comments(created_at)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_annotations_comment_id ON document_annotations(comment_id)")
        
        conn.commit()
        print("Migration completed successfully!")
        
        # Verify the migration
        cur.execute("SELECT COUNT(*) FROM document_comments")
        comments_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM document_annotations")
        annotations_count = cur.fetchone()[0]
        
        print(f"Final counts - Comments: {comments_count}, Annotations: {annotations_count}")
        
        # Show sample of migrated data
        cur.execute("""
            SELECT dc.document_id, dc.document_name, pd.document_number 
            FROM document_comments dc 
            JOIN plan_documents pd ON dc.document_id = pd.document_id 
            LIMIT 3
        """)
        sample_data = cur.fetchall()
        print(f"Sample migrated data: {sample_data}")
        
        cur.close()
        return True
        
    except Exception as e:
        print(f"Migration failed: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False

if __name__ == "__main__":
    print("Database Schema Migration with Cleanup")
    print("=" * 45)
    
    success = apply_migration_with_cleanup()
    
    if success:
        print("\n[SUCCESS] Migration completed successfully!")
        print("The document_comments and document_annotations tables now:")
        print("- Use INTEGER document_id instead of VARCHAR")
        print("- Have proper foreign key relationships to plan_documents")
        print("- Include proper constraints and indexes")
        print("- Orphaned records have been cleaned up")
    else:
        print("\n[ERROR] Migration failed. Please check the error messages above.")
