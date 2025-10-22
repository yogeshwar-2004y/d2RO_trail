#!/usr/bin/env python3
"""
Migration script to fix document_comments and document_annotations tables
This script will:
1. Change document_id from VARCHAR(255) to INT
2. Update foreign key references to use actual document_id from plan_documents
3. Add proper foreign key constraints
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_db_connection

def run_migration():
    """Run the migration to fix document_comments and document_annotations schema"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("Starting migration for document_comments and document_annotations tables...")
        
        # Step 1: Check if tables exist
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
        
        if not comments_exists or not annotations_exists:
            print("Tables don't exist yet. Creating them with correct schema...")
            # Import and run the database init function
            from utils.database_init import create_comments_tables
            create_comments_tables()
            print("Tables created successfully with correct schema.")
            return True
        
        # Step 2: Check current schema
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'document_comments' AND column_name = 'document_id'
        """)
        comments_schema = cur.fetchone()
        
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'document_annotations' AND column_name = 'document_id'
        """)
        annotations_schema = cur.fetchone()
        
        if comments_schema and comments_schema[1] == 'integer' and annotations_schema and annotations_schema[1] == 'integer':
            print("Tables already have correct schema (document_id is INTEGER). No migration needed.")
            return True
        
        print(f"Current schema - Comments: {comments_schema}, Annotations: {annotations_schema}")
        print("Migration needed. Proceeding with schema update...")
        
        # Step 3: Create backup tables
        print("Creating backup tables...")
        cur.execute("CREATE TABLE IF NOT EXISTS document_comments_backup AS SELECT * FROM document_comments")
        cur.execute("CREATE TABLE IF NOT EXISTS document_annotations_backup AS SELECT * FROM document_annotations")
        
        # Step 4: Drop existing tables
        print("Dropping existing tables...")
        cur.execute("DROP TABLE IF EXISTS document_annotations CASCADE")
        cur.execute("DROP TABLE IF EXISTS document_comments CASCADE")
        
        # Step 5: Recreate tables with correct schema
        print("Creating tables with correct schema...")
        cur.execute("""
            CREATE TABLE document_comments (
                comment_id SERIAL PRIMARY KEY,
                document_id INT NOT NULL REFERENCES plan_documents(document_id) ON DELETE CASCADE,
                document_name VARCHAR(255) NOT NULL,
                version VARCHAR(50),
                reviewer_id INTEGER,
                page_no INTEGER,
                section VARCHAR(255),
                description TEXT NOT NULL,
                commented_by VARCHAR(255) NOT NULL,
                is_annotation BOOLEAN DEFAULT FALSE,
                status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
                justification TEXT,
                accepted_by INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
                designer_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
                accepted_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            CREATE TABLE document_annotations (
                annotation_id SERIAL PRIMARY KEY,
                comment_id INTEGER REFERENCES document_comments(comment_id) ON DELETE CASCADE,
                document_id INT NOT NULL REFERENCES plan_documents(document_id) ON DELETE CASCADE,
                page_no INTEGER NOT NULL,
                x_position DECIMAL(10,2) NOT NULL,
                y_position DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Step 6: Migrate data
        print("Migrating data from backup tables...")
        
        # Migrate document_comments
        cur.execute("""
            INSERT INTO document_comments (
                comment_id, document_id, document_name, version, reviewer_id,
                page_no, section, description, commented_by, is_annotation,
                status, justification, accepted_by, accepted_at,
                created_at, updated_at
            )
            SELECT 
                dc.comment_id,
                pd.document_id,
                dc.document_name,
                dc.version,
                dc.reviewer_id,
                dc.page_no,
                dc.section,
                dc.description,
                dc.commented_by,
                dc.is_annotation,
                dc.status,
                dc.justification,
                dc.accepted_by,
                dc.accepted_at,
                dc.created_at,
                dc.updated_at
            FROM document_comments_backup dc
            LEFT JOIN plan_documents pd ON dc.document_id = pd.document_number
            WHERE pd.document_id IS NOT NULL
        """)
        
        comments_migrated = cur.rowcount
        print(f"Migrated {comments_migrated} comments")
        
        # Migrate document_annotations
        cur.execute("""
            INSERT INTO document_annotations (
                annotation_id, comment_id, document_id, page_no,
                x_position, y_position, created_at
            )
            SELECT 
                da.annotation_id,
                da.comment_id,
                pd.document_id,
                da.page_no,
                da.x_position,
                da.y_position,
                da.created_at
            FROM document_annotations_backup da
            LEFT JOIN plan_documents pd ON da.document_id = pd.document_number
            WHERE pd.document_id IS NOT NULL
        """)
        
        annotations_migrated = cur.rowcount
        print(f"Migrated {annotations_migrated} annotations")
        
        # Step 7: Create indexes
        print("Creating indexes...")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_comments_document_id ON document_comments(document_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_comments_status ON document_comments(status)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_comments_created_at ON document_comments(created_at)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_annotations_document_id ON document_annotations(document_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_document_annotations_comment_id ON document_annotations(comment_id)")
        
        # Step 8: Commit changes
        conn.commit()
        print("Migration completed successfully!")
        
        # Step 9: Verify migration
        cur.execute("SELECT COUNT(*) FROM document_comments")
        comments_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM document_annotations")
        annotations_count = cur.fetchone()[0]
        
        print(f"Final counts - Comments: {comments_count}, Annotations: {annotations_count}")
        
        # Step 10: Clean up backup tables (optional)
        response = input("Do you want to delete the backup tables? (y/N): ")
        if response.lower() == 'y':
            cur.execute("DROP TABLE IF EXISTS document_comments_backup")
            cur.execute("DROP TABLE IF EXISTS document_annotations_backup")
            conn.commit()
            print("Backup tables deleted.")
        else:
            print("Backup tables kept for safety.")
        
        cur.close()
        return True
        
    except Exception as e:
        print(f"Migration failed: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
        return False

if __name__ == "__main__":
    print("Document Comments and Annotations Schema Migration")
    print("=" * 50)
    
    success = run_migration()
    
    if success:
        print("\n[SUCCESS] Migration completed successfully!")
        print("The document_comments and document_annotations tables now:")
        print("- Use INTEGER document_id instead of VARCHAR")
        print("- Have proper foreign key relationships to plan_documents")
        print("- Include proper constraints and indexes")
    else:
        print("\n[ERROR] Migration failed. Please check the error messages above.")
        sys.exit(1)
