-- Migration script to fix document_comments and document_annotations tables
-- Changes:
-- 1. Change document_id from VARCHAR(255) to INT
-- 2. Update foreign key references to use actual document_id from plan_documents
-- 3. Add proper foreign key constraints

-- Step 1: Create temporary tables to store existing data
CREATE TABLE IF NOT EXISTS document_comments_backup AS 
SELECT * FROM document_comments;

CREATE TABLE IF NOT EXISTS document_annotations_backup AS 
SELECT * FROM document_annotations;

-- Step 2: Drop existing tables (this will also drop foreign key constraints)
DROP TABLE IF EXISTS document_annotations CASCADE;
DROP TABLE IF EXISTS document_comments CASCADE;

-- Step 3: Recreate document_comments table with correct schema
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
);

-- Step 4: Recreate document_annotations table with correct schema
CREATE TABLE document_annotations (
    annotation_id SERIAL PRIMARY KEY,
    comment_id INTEGER REFERENCES document_comments(comment_id) ON DELETE CASCADE,
    document_id INT NOT NULL REFERENCES plan_documents(document_id) ON DELETE CASCADE,
    page_no INTEGER NOT NULL,
    x_position DECIMAL(10,2) NOT NULL,
    y_position DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 5: Migrate data from backup tables
-- First, migrate document_comments data
INSERT INTO document_comments (
    comment_id,
    document_id,
    document_name,
    version,
    reviewer_id,
    page_no,
    section,
    description,
    commented_by,
    is_annotation,
    status,
    justification,
    accepted_by,
    designer_id,
    accepted_at,
    created_at,
    updated_at
)
SELECT 
    dc.comment_id,
    pd.document_id,  -- Use actual document_id from plan_documents
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
    dc.designer_id,
    dc.accepted_at,
    dc.created_at,
    dc.updated_at
FROM document_comments_backup dc
LEFT JOIN plan_documents pd ON dc.document_id = pd.document_number  -- Match by document_number
WHERE pd.document_id IS NOT NULL;  -- Only migrate records that have matching documents

-- Step 6: Migrate document_annotations data
INSERT INTO document_annotations (
    annotation_id,
    comment_id,
    document_id,
    page_no,
    x_position,
    y_position,
    created_at
)
SELECT 
    da.annotation_id,
    da.comment_id,
    pd.document_id,  -- Use actual document_id from plan_documents
    da.page_no,
    da.x_position,
    da.y_position,
    da.created_at
FROM document_annotations_backup da
LEFT JOIN plan_documents pd ON da.document_id = pd.document_number  -- Match by document_number
WHERE pd.document_id IS NOT NULL;  -- Only migrate records that have matching documents

-- Step 7: Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_document_comments_document_id ON document_comments(document_id);
CREATE INDEX IF NOT EXISTS idx_document_comments_status ON document_comments(status);
CREATE INDEX IF NOT EXISTS idx_document_comments_created_at ON document_comments(created_at);
CREATE INDEX IF NOT EXISTS idx_document_annotations_document_id ON document_annotations(document_id);
CREATE INDEX IF NOT EXISTS idx_document_annotations_comment_id ON document_annotations(comment_id);

-- Step 8: Clean up backup tables (optional - comment out if you want to keep backups)
-- DROP TABLE IF EXISTS document_comments_backup;
-- DROP TABLE IF EXISTS document_annotations_backup;

-- Step 9: Add comments for documentation
COMMENT ON TABLE document_comments IS 'Comments and annotations for plan documents with proper foreign key relationships';
COMMENT ON TABLE document_annotations IS 'Positional annotations for document comments with proper foreign key relationships';
COMMENT ON COLUMN document_comments.document_id IS 'Foreign key reference to plan_documents.document_id (integer)';
COMMENT ON COLUMN document_annotations.document_id IS 'Foreign key reference to plan_documents.document_id (integer)';
