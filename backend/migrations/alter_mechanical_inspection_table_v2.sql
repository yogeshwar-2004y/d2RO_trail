-- Migration: Alter mechanical inspection report table to match MechanicalInspection.vue UI
-- Date: 2025-01-15
-- Description: Updates existing table to match the current frontend form structure

-- 1. Drop old columns that are no longer needed
ALTER TABLE mechanical_inspection_report 
DROP COLUMN IF EXISTS document_no,
DROP COLUMN IF EXISTS date_of_issue,
DROP COLUMN IF EXISTS issue_level,
DROP COLUMN IF EXISTS customer_name,
DROP COLUMN IF EXISTS memo_id,
DROP COLUMN IF EXISTS product_name,
DROP COLUMN IF EXISTS sl_no,
DROP COLUMN IF EXISTS test_started_on,
DROP COLUMN IF EXISTS test_ended_on;

-- 2. Add new columns for the current UI structure
ALTER TABLE mechanical_inspection_report 
ADD COLUMN IF NOT EXISTS memo_ref_no VARCHAR(100),
ADD COLUMN IF NOT EXISTS lru_name TEXT,
ADD COLUMN IF NOT EXISTS inspection_stage TEXT,
ADD COLUMN IF NOT EXISTS test_venue TEXT,
ADD COLUMN IF NOT EXISTS sl_nos TEXT,
ADD COLUMN IF NOT EXISTS dated1 DATE,
ADD COLUMN IF NOT EXISTS dated2 DATE,
ADD COLUMN IF NOT EXISTS start_date DATE,
ADD COLUMN IF NOT EXISTS end_date DATE;

-- 3. Update parameter columns to include names with defaults (if not already present)
ALTER TABLE mechanical_inspection_report 
ADD COLUMN IF NOT EXISTS param1_name TEXT DEFAULT 'Burrs',
ADD COLUMN IF NOT EXISTS param2_name TEXT DEFAULT 'Damages',
ADD COLUMN IF NOT EXISTS param3_name TEXT DEFAULT 'Name Plate',
ADD COLUMN IF NOT EXISTS param4_name TEXT DEFAULT 'Engraving',
ADD COLUMN IF NOT EXISTS param5_name TEXT DEFAULT 'Passivation',
ADD COLUMN IF NOT EXISTS param6_name TEXT DEFAULT 'Chromate',
ADD COLUMN IF NOT EXISTS param7_name TEXT DEFAULT 'Electro-less Nickel plating',
ADD COLUMN IF NOT EXISTS param8_name TEXT DEFAULT 'Fasteners';

-- 4. Add comments to document the changes
COMMENT ON COLUMN mechanical_inspection_report.project_name IS 'Project Name from form';
COMMENT ON COLUMN mechanical_inspection_report.report_ref_no IS 'Report Reference Number';
COMMENT ON COLUMN mechanical_inspection_report.memo_ref_no IS 'Memo Reference Number';
COMMENT ON COLUMN mechanical_inspection_report.lru_name IS 'LRU (Line Replaceable Unit) Name';
COMMENT ON COLUMN mechanical_inspection_report.inspection_stage IS 'Stage of inspection';
COMMENT ON COLUMN mechanical_inspection_report.test_venue IS 'Location where test was conducted';
COMMENT ON COLUMN mechanical_inspection_report.sl_nos IS 'Serial Numbers';
COMMENT ON COLUMN mechanical_inspection_report.dp_name IS 'DP Name from form';
COMMENT ON COLUMN mechanical_inspection_report.dated1 IS 'First date field (next to Report Ref No)';
COMMENT ON COLUMN mechanical_inspection_report.dated2 IS 'Second date field (next to Memo Ref No)';
COMMENT ON COLUMN mechanical_inspection_report.sru_name IS 'SRU Name';
COMMENT ON COLUMN mechanical_inspection_report.part_no IS 'Part Number';
COMMENT ON COLUMN mechanical_inspection_report.quantity IS 'Quantity';
COMMENT ON COLUMN mechanical_inspection_report.start_date IS 'Test start date';
COMMENT ON COLUMN mechanical_inspection_report.end_date IS 'Test end date';

-- 5. Verify the table structure
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'mechanical_inspection_report' 
ORDER BY ordinal_position;
