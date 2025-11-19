-- Migration to add project management fields to projects table
-- This adds: project_director, deputy_project_director, and qa_manager
-- All fields support text with spaces

-- Add the project_director column
ALTER TABLE projects ADD COLUMN IF NOT EXISTS project_director VARCHAR(100);

-- Add the deputy_project_director column
ALTER TABLE projects ADD COLUMN IF NOT EXISTS deputy_project_director VARCHAR(100);

-- Add the qa_manager column
ALTER TABLE projects ADD COLUMN IF NOT EXISTS qa_manager VARCHAR(100);

-- Add comments to document the purpose of these fields
COMMENT ON COLUMN projects.project_director IS 'Project Director name - supports text with spaces';
COMMENT ON COLUMN projects.deputy_project_director IS 'Deputy Project Director name - supports text with spaces';
COMMENT ON COLUMN projects.qa_manager IS 'QA Manager name - supports text with spaces';

