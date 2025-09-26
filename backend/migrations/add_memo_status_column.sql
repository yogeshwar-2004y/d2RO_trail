-- Migration: Add memo_status column to memos table
-- Date: 2025-01-07
-- Description: Adds memo_status field with enum values and sets default to 'not assigned'

-- Add memo_status column with enum constraint
ALTER TABLE memos 
ADD COLUMN memo_status VARCHAR(20) DEFAULT 'not assigned' 
CHECK (memo_status IN ('not assigned', 'assigned', 'disapproved'));

-- Update existing memos to have appropriate status based on current data
-- If memo has been accepted, set status to 'assigned'
UPDATE memos 
SET memo_status = 'assigned' 
WHERE accepted_at IS NOT NULL;

-- If memo has been rejected (exists in memo_approval with status 'rejected'), set status to 'disapproved'
UPDATE memos 
SET memo_status = 'disapproved' 
WHERE memo_id IN (
    SELECT memo_id 
    FROM memo_approval 
    WHERE status = 'rejected'
);

-- Add comment to the column for documentation
COMMENT ON COLUMN memos.memo_status IS 'Status of the memo: not assigned, assigned, or disapproved';
