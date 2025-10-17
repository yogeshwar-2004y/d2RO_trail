-- Create tech_support_requests table
CREATE TABLE IF NOT EXISTS tech_support_requests (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    issue_description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on user_id for better performance
CREATE INDEX IF NOT EXISTS idx_tech_support_user_id ON tech_support_requests(user_id);

-- Create index on status for filtering
CREATE INDEX IF NOT EXISTS idx_tech_support_status ON tech_support_requests(status);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_tech_support_created_at ON tech_support_requests(created_at);
