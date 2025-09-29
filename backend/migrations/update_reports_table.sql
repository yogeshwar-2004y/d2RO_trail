-- Migration: Update reports table to support memo-based reports
-- Date: 2025-01-15
-- Description: Adds memo_id, status, and created_at fields to reports table

-- Add new columns to reports table
ALTER TABLE reports 
ADD COLUMN memo_id INT REFERENCES memos(memo_id) ON DELETE CASCADE,
ADD COLUMN status VARCHAR(50) DEFAULT 'ASSIGNED' 
    CHECK (status IN ('ASSIGNED', 'SUCCESSFULLY COMPLETED', 'TEST NOT CONDUCTED', 'TEST FAILED')),
ADD COLUMN created_at TIMESTAMP DEFAULT NOW();

-- Add comment to the new columns for documentation
COMMENT ON COLUMN reports.memo_id IS 'Reference to the memo that this report is based on';
COMMENT ON COLUMN reports.status IS 'Status of the report: ASSIGNED, SUCCESSFULLY COMPLETED, TEST NOT CONDUCTED, TEST FAILED';
COMMENT ON COLUMN reports.created_at IS 'Timestamp when the report was created';
