-- Migration: Add 'COMPLETED WITH OBSERVATIONS' status to reports table
-- Date: 2025-01-XX
-- Description: Adds 'COMPLETED WITH OBSERVATIONS' as a valid status value for reports table

-- Drop the existing constraint if it exists
ALTER TABLE reports 
DROP CONSTRAINT IF EXISTS reports_status_check;

-- Add the new constraint with 'COMPLETED WITH OBSERVATIONS' included
ALTER TABLE reports 
ADD CONSTRAINT reports_status_check 
CHECK (status IN ('ASSIGNED', 'SUCCESSFULLY COMPLETED', 'TEST NOT CONDUCTED', 'TEST FAILED', 'COMPLETED WITH OBSERVATIONS'));

-- Add comment to document the change
COMMENT ON COLUMN reports.status IS 'Status of the report: ASSIGNED, SUCCESSFULLY COMPLETED, TEST NOT CONDUCTED, TEST FAILED, COMPLETED WITH OBSERVATIONS';

