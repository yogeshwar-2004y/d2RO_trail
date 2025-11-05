-- Migration: Add report_card_id to inspection report tables
-- This links inspection reports to their parent report cards (reports table)
-- Similar to mechanical_inspection_report.report_card_id

-- ============================================================
-- 1. Conformal Coating Inspection Report
-- ============================================================
-- Add report_card_id column to link with reports table
ALTER TABLE conformal_coating_inspection_report 
ADD COLUMN IF NOT EXISTS report_card_id INT REFERENCES reports(report_id) ON DELETE CASCADE;

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_conformal_coating_report_card_id 
ON conformal_coating_inspection_report(report_card_id);

-- Add comment to document the field
COMMENT ON COLUMN conformal_coating_inspection_report.report_card_id 
IS 'References the report card (reports.report_id) that this conformal coating inspection report belongs to';

-- Migrate data from original_report_id to report_card_id if original_report_id exists
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'conformal_coating_inspection_report' 
        AND column_name = 'original_report_id'
    ) THEN
        UPDATE conformal_coating_inspection_report 
        SET report_card_id = original_report_id 
        WHERE report_card_id IS NULL AND original_report_id IS NOT NULL;
        
        RAISE NOTICE 'Migrated data from original_report_id to report_card_id for conformal_coating_inspection_report';
    END IF;
END $$;

-- ============================================================
-- 2. Kit of Parts Inspection Report
-- ============================================================
-- Add report_card_id column to link with reports table
ALTER TABLE kit_of_parts_inspection_report 
ADD COLUMN IF NOT EXISTS report_card_id INT REFERENCES reports(report_id) ON DELETE CASCADE;

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_kit_of_parts_report_card_id 
ON kit_of_parts_inspection_report(report_card_id);

-- Add comment to document the field
COMMENT ON COLUMN kit_of_parts_inspection_report.report_card_id 
IS 'References the report card (reports.report_id) that this kit of parts inspection report belongs to';

-- Migrate data from original_report_id to report_card_id if original_report_id exists
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'kit_of_parts_inspection_report' 
        AND column_name = 'original_report_id'
    ) THEN
        UPDATE kit_of_parts_inspection_report 
        SET report_card_id = original_report_id 
        WHERE report_card_id IS NULL AND original_report_id IS NOT NULL;
        
        RAISE NOTICE 'Migrated data from original_report_id to report_card_id for kit_of_parts_inspection_report';
    END IF;
END $$;

