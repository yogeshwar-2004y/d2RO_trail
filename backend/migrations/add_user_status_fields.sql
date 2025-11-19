-- Migration: Add deleted and enabled columns to users table
-- This allows soft delete (users remain in DB but hidden from UI)
-- and enable/disable functionality (users cannot login when disabled)

-- Add deleted column (soft delete flag)
ALTER TABLE users ADD COLUMN IF NOT EXISTS deleted BOOLEAN DEFAULT FALSE;
COMMENT ON COLUMN users.deleted IS 'Soft delete flag - when true, user is deleted but records remain';

-- Add enabled column (enable/disable toggle)
ALTER TABLE users ADD COLUMN IF NOT EXISTS enabled BOOLEAN DEFAULT TRUE;
COMMENT ON COLUMN users.enabled IS 'Enable/disable flag - when false, user cannot login';

-- Create index on deleted for better query performance
CREATE INDEX IF NOT EXISTS idx_users_deleted ON users(deleted);

-- Create index on enabled for better query performance
CREATE INDEX IF NOT EXISTS idx_users_enabled ON users(enabled);

