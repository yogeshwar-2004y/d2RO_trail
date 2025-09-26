-- Migration: Fix memo_approval user_id column to allow NULL values
-- Date: 2025-09-26
-- Description: Allows user_id to be NULL in memo_approval table for rejected memos

-- Drop the NOT NULL constraint on user_id column
ALTER TABLE memo_approval 
ALTER COLUMN user_id DROP NOT NULL;

-- Add a comment to document the change
COMMENT ON COLUMN memo_approval.user_id IS 'User ID of the reviewer (NULL for rejected memos)';
