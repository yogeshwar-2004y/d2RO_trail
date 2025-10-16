-- Create login_logs table
CREATE TABLE IF NOT EXISTS login_logs (
    serial_num SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    activity_performed VARCHAR(100) NOT NULL, -- 'LOGIN' or 'LOGOUT'
    performed_by INTEGER NOT NULL, -- Same as user_id for self-login/logout
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_login_logs_user_id ON login_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_login_logs_timestamp ON login_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_login_logs_activity ON login_logs(activity_performed);
