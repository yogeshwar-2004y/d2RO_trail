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
                commented_by VARCHAR(255) NOT NULL,
                is_annotation BOOLEAN DEFAULT FALSE,
                status VARCHAR(20) DEFAULT 'pending',
                justification TEXT,
                accepted_by VARCHAR(255),
                designer_id INTEGER,
                accepted_at TIMESTAMP,
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
        
        # Add missing commented_by column if it doesn't exist
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='document_comments' AND column_name='commented_by') THEN
                    ALTER TABLE document_comments ADD COLUMN commented_by VARCHAR(100) DEFAULT 'Anonymous';
                END IF;
            END $$;
        """)
        
        conn.commit()
        cur.close()
        print("Comments and annotations tables created/verified successfully")
        
    except Exception as e:
        print(f"Error creating comments tables: {str(e)}")

def create_memos_tables():
    """Create memos, memo_references, and memo_approval tables if they don't exist"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create memos table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS memos (
                memo_id SERIAL PRIMARY KEY,
                from_person TEXT NOT NULL,
                to_person TEXT NOT NULL,
                thru_person TEXT,
                casdic_ref_no VARCHAR,
                dated DATE,
                wing_proj_ref_no VARCHAR,
                lru_sru_desc TEXT,
                part_number VARCHAR,
                slno_units TEXT[],
                qty_offered INT,
                manufacturer VARCHAR(255),
                drawing_no_rev TEXT,
                source TEXT,
                unit_identification TEXT[],
                mechanical_inspn TEXT,
                inspn_test_stage_offered TEXT,
                stte_status TEXT,
                test_stage_cleared TEXT,
                venue TEXT,
                memo_date DATE,
                name_designation TEXT,
                coordinator TEXT,
                test_facility VARCHAR(255),
                test_cycle_duration TEXT,
                test_start_on TIMESTAMP,
                test_complete_on TIMESTAMP,
                calibration_status TEXT,
                func_check_initial TIMESTAMP,
                perf_check_during TIMESTAMP,
                func_check_end TIMESTAMP,
                certified TEXT[],
                remarks TEXT,
                submitted_at TIMESTAMP,
                submitted_by INT REFERENCES users(user_id) ON DELETE CASCADE,
                accepted_at TIMESTAMP,
                accepted_by INT REFERENCES users(user_id) ON DELETE CASCADE,
                memo_status VARCHAR(50) NOT NULL DEFAULT 'not_assigned'
                    CHECK (memo_status IN ('not_assigned', 'assigned', 'disapproved', 'successfully_completed', 'test_not_conducted', 'completed_with_observations', 'test_failed')),
                qa_remarks TEXT
            )
        """)
        
        # Create memo_references table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS memo_references (
                ref_id SERIAL PRIMARY KEY,
                memo_id INT REFERENCES memos(memo_id) ON DELETE CASCADE,
                ref_doc VARCHAR(255),
                ref_no VARCHAR(255),
                ver FLOAT,
                rev FLOAT
            )
        """)
        
        # Create memo_approval table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS memo_approval (
                approval_id SERIAL PRIMARY KEY,
                memo_id INT REFERENCES memos(memo_id) ON DELETE CASCADE,
                user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                approved_by INT REFERENCES users(user_id) ON DELETE CASCADE,
                status VARCHAR(20) NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'accepted', 'rejected')),
                approval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                comments TEXT
            )
        """)
        
        # Create reports table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                report_id SERIAL PRIMARY KEY,
                memo_id INT REFERENCES memos(memo_id) ON DELETE CASCADE,
                status VARCHAR(50) DEFAULT 'ASSIGNED' 
                    CHECK (status IN ('ASSIGNED', 'SUCCESSFULLY COMPLETED', 'TEST NOT CONDUCTED', 'TEST FAILED')),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Add memo_status column if it doesn't exist (for existing tables)
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='memos' AND column_name='memo_status') THEN
                    ALTER TABLE memos ADD COLUMN memo_status VARCHAR(50) DEFAULT 'not_assigned' 
                        CHECK (memo_status IN ('not_assigned', 'assigned', 'disapproved', 'successfully_completed', 'test_not_conducted', 'completed_with_observations', 'test_failed'));
                END IF;
            END $$;
        """)
        
        # Add coordinator column if it doesn't exist (for existing tables)
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='memos' AND column_name='coordinator') THEN
                    ALTER TABLE memos ADD COLUMN coordinator TEXT;
                END IF;
            END $$;
        """)
        
        # Add approved_by column to memo_approval if it doesn't exist (for existing tables)
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='memo_approval' AND column_name='approved_by') THEN
                    ALTER TABLE memo_approval ADD COLUMN approved_by INT REFERENCES users(user_id) ON DELETE CASCADE;
                END IF;
            END $$;
        """)
        
        # Add status column to memo_approval if it doesn't exist (for existing tables)
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='memo_approval' AND column_name='status') THEN
                    ALTER TABLE memo_approval ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'accepted', 'rejected'));
                END IF;
            END $$;
        """)
        
        # Add approval_date column to memo_approval if it doesn't exist (for existing tables)
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='memo_approval' AND column_name='approval_date') THEN
                    ALTER TABLE memo_approval ADD COLUMN approval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
            END $$;
        """)
        
        # Fix memo_status constraint to use spaces instead of underscores
        cur.execute("""
            DO $$ 
            BEGIN 
                -- Drop the existing constraint if it exists
                IF EXISTS (SELECT 1 FROM information_schema.check_constraints 
                          WHERE constraint_name = 'memos_memo_status_check') THEN
                    ALTER TABLE memos DROP CONSTRAINT memos_memo_status_check;
                END IF;
                
                -- Add the new constraint with correct values
                ALTER TABLE memos ADD CONSTRAINT memos_memo_status_check 
                    CHECK (memo_status IN ('not_assigned', 'assigned', 'disapproved', 'successfully_completed', 'test_not_conducted', 'completed_with_observations', 'test_failed'));
            END $$;
        """)
        
        # Add qa_remarks column if it doesn't exist
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='memos' AND column_name='qa_remarks') THEN
                    ALTER TABLE memos ADD COLUMN qa_remarks TEXT;
                END IF;
            END $$;
        """)
        
        conn.commit()
        cur.close()
        print("Memos tables created/verified successfully")
        
    except Exception as e:
        print(f"Error creating memos tables: {str(e)}")

def initialize_database():
    """Initialize all database tables and setup"""
    create_news_table()
    create_comments_tables()
    create_memos_tables()
    print("Database initialization completed")
