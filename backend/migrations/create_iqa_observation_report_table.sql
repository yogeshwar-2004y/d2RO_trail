-- Migration: Create IQA observation report table
-- Date: 2025-01-15
-- Description: Creates table for IQA observation reports based on ObservationReport.vue component

-- 1. Create the IQA observation report table
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
);

-- 2. Create index on foreign keys for better query performance
CREATE INDEX IF NOT EXISTS idx_iqa_report_project_id ON iqa_observation_reports(project_id);
CREATE INDEX IF NOT EXISTS idx_iqa_report_lru_id ON iqa_observation_reports(lru_id);
CREATE INDEX IF NOT EXISTS idx_iqa_report_document_id ON iqa_observation_reports(document_id);
CREATE INDEX IF NOT EXISTS idx_iqa_report_created_by ON iqa_observation_reports(created_by);
CREATE INDEX IF NOT EXISTS idx_iqa_report_reviewed_by ON iqa_observation_reports(reviewed_by_user_id);
CREATE INDEX IF NOT EXISTS idx_iqa_report_approved_by ON iqa_observation_reports(approved_by_user_id);
CREATE INDEX IF NOT EXISTS idx_iqa_report_date ON iqa_observation_reports(report_date);

-- 3. Create a function to update the updated_at column (if not exists)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 4. Create the trigger for updated_at
DROP TRIGGER IF EXISTS trg_update_updated_at_iqa_report ON iqa_observation_reports;
CREATE TRIGGER trg_update_updated_at_iqa_report
BEFORE UPDATE ON iqa_observation_reports
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- 5. Add comments for documentation
COMMENT ON TABLE iqa_observation_reports IS 'IQA observation reports based on ObservationReport.vue component';
COMMENT ON COLUMN iqa_observation_reports.project_id IS 'Foreign key to projects table';
COMMENT ON COLUMN iqa_observation_reports.lru_id IS 'Foreign key to lrus table';
COMMENT ON COLUMN iqa_observation_reports.document_id IS 'Foreign key to plan_documents table - the selected document version';
COMMENT ON COLUMN iqa_observation_reports.observation_count IS 'Observation count identifier (e.g., OBS-001)';
COMMENT ON COLUMN iqa_observation_reports.report_date IS 'Date when the report was created';
COMMENT ON COLUMN iqa_observation_reports.current_year IS 'Current year for the report';
COMMENT ON COLUMN iqa_observation_reports.lru_part_number IS 'LRU Part Number (user input)';
COMMENT ON COLUMN iqa_observation_reports.serial_number IS 'Serial Number (user input)';
COMMENT ON COLUMN iqa_observation_reports.inspection_stage IS 'Inspection stage (default: Document review/report)';
COMMENT ON COLUMN iqa_observation_reports.doc_review_date IS 'Date of document review';
COMMENT ON COLUMN iqa_observation_reports.review_venue IS 'Review venue location';
COMMENT ON COLUMN iqa_observation_reports.reference_document IS 'Reference document information';
COMMENT ON COLUMN iqa_observation_reports.reviewed_by_user_id IS 'User ID of the person who reviewed (from signature verification)';
COMMENT ON COLUMN iqa_observation_reports.reviewed_by_signature_path IS 'Path to the reviewed by signature image';
COMMENT ON COLUMN iqa_observation_reports.reviewed_by_verified_name IS 'Verified name of the reviewer from signature authentication';
COMMENT ON COLUMN iqa_observation_reports.approved_by_user_id IS 'User ID of the person who approved (from signature verification)';
COMMENT ON COLUMN iqa_observation_reports.approved_by_signature_path IS 'Path to the approved by signature image';
COMMENT ON COLUMN iqa_observation_reports.approved_by_verified_name IS 'Verified name of the approver from signature authentication';
COMMENT ON COLUMN iqa_observation_reports.created_by IS 'User ID who created this report';
COMMENT ON COLUMN iqa_observation_reports.created_at IS 'Timestamp when the report was created';
COMMENT ON COLUMN iqa_observation_reports.updated_at IS 'Timestamp when the report was last updated';

