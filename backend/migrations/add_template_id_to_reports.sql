-- Migration: Add template_id field to reports table
-- This migration adds a template_id field to link reports with their selected templates

-- Add template_id column to reports table
ALTER TABLE reports 
ADD COLUMN template_id INT REFERENCES report_templates(template_id) ON DELETE SET NULL;

-- Add index for better query performance
CREATE INDEX IF NOT EXISTS idx_reports_template_id ON reports(template_id);

-- Add comment to document the field
COMMENT ON COLUMN reports.template_id IS 'References the selected report template for this report';
