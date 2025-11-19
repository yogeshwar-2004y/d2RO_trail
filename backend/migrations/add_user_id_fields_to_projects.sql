-- Migration to add user_id fields for project management roles
-- This allows linking to users table OR storing text names manually

-- Add user_id columns for project management roles
ALTER TABLE projects ADD COLUMN IF NOT EXISTS project_director_id INT REFERENCES users(user_id) ON DELETE SET NULL;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS deputy_project_director_id INT REFERENCES users(user_id) ON DELETE SET NULL;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS qa_manager_id INT REFERENCES users(user_id) ON DELETE SET NULL;

-- Add comments to document the purpose of these fields
COMMENT ON COLUMN projects.project_director_id IS 'User ID of Project Director (if selected from users list), NULL if manually entered';
COMMENT ON COLUMN projects.deputy_project_director_id IS 'User ID of Deputy Project Director (if selected from users list), NULL if manually entered';
COMMENT ON COLUMN projects.qa_manager_id IS 'User ID of QA Manager (if selected from users list), NULL if manually entered';

