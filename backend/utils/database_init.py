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
        
        # Create document_comments table with proper foreign key to plan_documents
        cur.execute("""
            CREATE TABLE IF NOT EXISTS document_comments (
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
        
        # Create document_annotations table with proper foreign key to plan_documents
        cur.execute("""
            CREATE TABLE IF NOT EXISTS document_annotations (
                annotation_id SERIAL PRIMARY KEY,
                comment_id INTEGER REFERENCES document_comments(comment_id) ON DELETE CASCADE,
                document_id INT NOT NULL REFERENCES plan_documents(document_id) ON DELETE CASCADE,
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
        
        # Update accepted_by column to INTEGER if it's currently VARCHAR
        cur.execute("""
            DO $$ 
            BEGIN 
                IF EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='document_comments' AND column_name='accepted_by' 
                          AND data_type='character varying') THEN
                    -- First, drop the old column and add the new one
                    ALTER TABLE document_comments DROP COLUMN IF EXISTS accepted_by;
                    ALTER TABLE document_comments ADD COLUMN accepted_by INTEGER;
                END IF;
            END $$;
        """)
        
        # Update status constraint to allow pending, accepted, rejected
        cur.execute("""
            DO $$ 
            BEGIN 
                -- Drop existing status constraint if it exists
                IF EXISTS (SELECT 1 FROM pg_constraint 
                          WHERE conname = 'document_comments_status_check') THEN
                    ALTER TABLE document_comments DROP CONSTRAINT document_comments_status_check;
                END IF;
                
                -- Add new constraint with correct values
                ALTER TABLE document_comments ADD CONSTRAINT document_comments_status_check 
                CHECK (status IN ('pending', 'accepted', 'rejected'));
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
                    CHECK (memo_status IN ('not_assigned', 'assigned', 'disapproved', 'rejected', 'successfully_completed', 'test_not_conducted', 'completed_with_observations', 'test_failed')),
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
                    CHECK (memo_status IN ('not_assigned', 'assigned', 'disapproved', 'rejected', 'successfully_completed', 'test_not_conducted', 'completed_with_observations', 'test_failed'));
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

def create_iqa_observation_report_table():
    """Create iqa_observation_reports table if it doesn't exist"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS iqa_observation_reports (
                report_id SERIAL PRIMARY KEY,
                
                -- Foreign keys
                project_id INT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
                lru_id INT NOT NULL REFERENCES lrus(lru_id) ON DELETE CASCADE,
                document_id INT REFERENCES plan_documents(document_id) ON DELETE SET NULL,
                
                -- Report identification
                observation_count VARCHAR(50),
                report_date DATE NOT NULL DEFAULT CURRENT_DATE,
                current_year VARCHAR(10),
                
                -- Document details (user inputs)
                lru_part_number VARCHAR(100),
                serial_number VARCHAR(100),
                inspection_stage VARCHAR(255) DEFAULT 'Document review/report',
                doc_review_date DATE,
                review_venue VARCHAR(255),
                reference_document TEXT,
                
                -- Signature information - Reviewed By
                reviewed_by_user_id INT REFERENCES users(user_id) ON DELETE SET NULL,
                reviewed_by_signature_path TEXT,
                reviewed_by_verified_name VARCHAR(255),
                
                -- Signature information - Approved By
                approved_by_user_id INT REFERENCES users(user_id) ON DELETE SET NULL,
                approved_by_signature_path TEXT,
                approved_by_verified_name VARCHAR(255),
                
                -- Metadata
                created_by INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for better query performance
        cur.execute("CREATE INDEX IF NOT EXISTS idx_iqa_report_project_id ON iqa_observation_reports(project_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_iqa_report_lru_id ON iqa_observation_reports(lru_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_iqa_report_document_id ON iqa_observation_reports(document_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_iqa_report_created_by ON iqa_observation_reports(created_by)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_iqa_report_reviewed_by ON iqa_observation_reports(reviewed_by_user_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_iqa_report_approved_by ON iqa_observation_reports(approved_by_user_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_iqa_report_date ON iqa_observation_reports(report_date)")
        
        # Create or replace the update trigger function
        cur.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Create trigger for updated_at
        cur.execute("""
            DROP TRIGGER IF EXISTS trg_update_updated_at_iqa_report ON iqa_observation_reports;
            CREATE TRIGGER trg_update_updated_at_iqa_report
            BEFORE UPDATE ON iqa_observation_reports
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
        """)
        
        conn.commit()
        cur.close()
        print("IQA observation reports table created/verified successfully")
        
    except Exception as e:
        print(f"Error creating IQA observation reports table: {str(e)}")

def initialize_database():
    """Initialize all database tables and setup"""
    create_news_table()
    create_comments_tables()
    create_memos_tables()
    create_iqa_observation_report_table()
    print("Database initialization completed")
