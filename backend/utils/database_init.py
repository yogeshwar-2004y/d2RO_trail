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

def initialize_database():
    """Initialize all database tables and setup"""
    create_news_table()
    print("Database initialization completed")
