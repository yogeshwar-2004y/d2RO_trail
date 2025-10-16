-- Add suspicious activity tracking columns to login_logs table
ALTER TABLE login_logs 
ADD COLUMN IF NOT EXISTS is_suspicious BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS suspicion_reason TEXT,
ADD COLUMN IF NOT EXISTS failed_attempts_count INTEGER DEFAULT 0;

-- Create index for suspicious activities
CREATE INDEX IF NOT EXISTS idx_login_logs_suspicious ON login_logs(is_suspicious);
CREATE INDEX IF NOT EXISTS idx_login_logs_timestamp_user ON login_logs(user_id, timestamp);
