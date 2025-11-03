-- Migration: Add report_card_id field to raw_material_inspection_report table
-- Date: 2025-01-20
-- Description: Adds report_card_id as a foreign key linking to the main reports table

-- Add report_card_id column to raw_material_inspection_report table
ALTER TABLE raw_material_inspection_report 
ADD COLUMN IF NOT EXISTS report_card_id INT REFERENCES reports(report_id) ON DELETE SET NULL;

-- Add index for better query performance
CREATE INDEX IF NOT EXISTS idx_raw_material_inspection_report_card_id ON raw_material_inspection_report(report_card_id);

-- Add comment to document the field
COMMENT ON COLUMN raw_material_inspection_report.report_card_id IS 'Foreign key linking to the main reports table (report_id)';

