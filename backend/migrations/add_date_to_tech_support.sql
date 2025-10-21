-- Add issue_date column to tech_support_requests table
ALTER TABLE tech_support_requests 
ADD COLUMN IF NOT EXISTS issue_date DATE;

-- Update existing records to use created_at date if issue_date is null
UPDATE tech_support_requests 
SET issue_date = DATE(created_at) 
WHERE issue_date IS NULL;

-- Make issue_date NOT NULL after updating existing records
ALTER TABLE tech_support_requests 
ALTER COLUMN issue_date SET NOT NULL;
