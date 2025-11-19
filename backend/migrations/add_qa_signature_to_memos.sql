-- Migration: Add qa_signature column to memos table
-- Date: 2025-01-XX
-- Description: Adds qa_signature column to store QA reviewer signature URL/path

-- Add qa_signature column to memos table
ALTER TABLE memos 
ADD COLUMN IF NOT EXISTS qa_signature TEXT;

-- Add a comment to document the column
COMMENT ON COLUMN memos.qa_signature IS 'QA reviewer signature URL or file path';

