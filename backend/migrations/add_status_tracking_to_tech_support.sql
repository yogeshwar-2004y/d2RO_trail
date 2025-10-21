-- Add status tracking fields to tech_support_requests table
ALTER TABLE tech_support_requests 
ADD COLUMN IF NOT EXISTS status_updated_by INTEGER;

ALTER TABLE tech_support_requests 
ADD COLUMN IF NOT EXISTS status_updated_at TIMESTAMP;

-- Add foreign key constraint for status_updated_by
ALTER TABLE tech_support_requests 
ADD CONSTRAINT fk_tech_support_status_updated_by 
FOREIGN KEY (status_updated_by) REFERENCES users(user_id);

-- Create index for better performance
CREATE INDEX IF NOT EXISTS idx_tech_support_status_updated_by ON tech_support_requests(status_updated_by);
CREATE INDEX IF NOT EXISTS idx_tech_support_status_updated_at ON tech_support_requests(status_updated_at);
