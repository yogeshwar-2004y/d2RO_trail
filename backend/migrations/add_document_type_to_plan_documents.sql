-- Migration: Add document_type column to plan_documents table
-- This links documents to their document types from the document_types table

-- Add document_type column (foreign key to document_types table)
ALTER TABLE plan_documents ADD COLUMN IF NOT EXISTS document_type INTEGER REFERENCES document_types(type_id) ON DELETE SET NULL;

-- Create index on document_type for better query performance
CREATE INDEX IF NOT EXISTS idx_plan_documents_document_type ON plan_documents(document_type);

COMMENT ON COLUMN plan_documents.document_type IS 'Foreign key to document_types table - categorizes the document type';

