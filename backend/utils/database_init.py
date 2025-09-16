"""
Database initialization utilities
"""
from config import get_db_connection

def create_news_table():
    """Create news_updates table if it doesn't exist"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS news_updates (
                id SERIAL PRIMARY KEY,
                news_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hidden BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Add updated_at column if it doesn't exist (for existing tables)
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='news_updates' AND column_name='updated_at') THEN
                    ALTER TABLE news_updates ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
            END $$;
        """)
        
        # Add hidden column if it doesn't exist (for existing tables)
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='news_updates' AND column_name='hidden') THEN
                    ALTER TABLE news_updates ADD COLUMN hidden BOOLEAN DEFAULT FALSE;
                END IF;
            END $$;
        """)
        
        conn.commit()
        cur.close()
        print("News updates table created/verified successfully")
        
    except Exception as e:
        print(f"Error creating news table: {str(e)}")

def create_comments_tables():
    """Create document_comments and document_annotations tables if they don't exist"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create document_comments table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS document_comments (
                comment_id SERIAL PRIMARY KEY,
                document_id VARCHAR(255) NOT NULL,
                document_name VARCHAR(255) NOT NULL,
                version VARCHAR(50),
                reviewer_id INTEGER,
                page_no INTEGER,
                section VARCHAR(255),
                description TEXT NOT NULL,
                author VARCHAR(255) NOT NULL,
                is_annotation BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create document_annotations table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS document_annotations (
                annotation_id SERIAL PRIMARY KEY,
                comment_id INTEGER REFERENCES document_comments(comment_id) ON DELETE CASCADE,
                document_id VARCHAR(255) NOT NULL,
                page_no INTEGER NOT NULL,
                x_position DECIMAL(10,2) NOT NULL,
                y_position DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cur.close()
        print("Comments and annotations tables created/verified successfully")
        
    except Exception as e:
        print(f"Error creating comments tables: {str(e)}")

def initialize_database():
    """Initialize all database tables and setup"""
    create_news_table()
    create_comments_tables()
    print("Database initialization completed")
