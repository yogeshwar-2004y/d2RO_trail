-- Add notification support to activity_logs table
ALTER TABLE activity_logs 
ADD COLUMN IF NOT EXISTS notified_user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
ADD COLUMN IF NOT EXISTS is_read BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS notification_type VARCHAR(50);

-- Create index for better query performance on notifications
CREATE INDEX IF NOT EXISTS idx_activity_logs_notified_user ON activity_logs(notified_user_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_is_read ON activity_logs(is_read);
CREATE INDEX IF NOT EXISTS idx_activity_logs_notification_type ON activity_logs(notification_type);

