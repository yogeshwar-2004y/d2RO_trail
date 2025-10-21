-- Create activity_logs table for tracking user activities
CREATE TABLE IF NOT EXISTS activity_logs (
    activity_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(project_id) ON DELETE CASCADE,
    activity_performed VARCHAR(100) NOT NULL,
    performed_by INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT NOW(),
    additional_info TEXT
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_activity_logs_project_id ON activity_logs(project_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_performed_by ON activity_logs(performed_by);
CREATE INDEX IF NOT EXISTS idx_activity_logs_timestamp ON activity_logs(timestamp);
