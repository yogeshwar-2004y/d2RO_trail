-- Migration: Add coordinator column to memos table
-- Date: 2025-01-27
-- Description: Adds a coordinator column to store coordinator information for memos

-- Add coordinator column to memos table
ALTER TABLE memos 
ADD COLUMN coordinator TEXT;

-- Add a comment to document the column
COMMENT ON COLUMN memos.coordinator IS 'Coordinator responsible for the memo';

-- Update existing records with a default value if needed
-- UPDATE memos SET coordinator = 'TBD' WHERE coordinator IS NULL;
