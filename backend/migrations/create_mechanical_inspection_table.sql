-- Migration: Create mechanical inspection report table
-- Date: 2025-01-15
-- Description: Creates table for mechanical inspection reports based on MechanicalInspection.vue

-- 1. Create the mechanical inspection report table
CREATE TABLE mechanical_inspection_report (
    report_id SERIAL PRIMARY KEY,

    -- Header info (from General Information section)
    project_name TEXT,
    report_ref_no VARCHAR(100),
    document_no VARCHAR(100),
    date_of_issue DATE,
    issue_level VARCHAR(50),
    customer_name TEXT,
    memo_id VARCHAR(100),
    product_name TEXT,
    dp_name TEXT,
    sl_no VARCHAR(100),
    sru_name TEXT,
    part_no VARCHAR(100),
    quantity INT,

    -- Test Timeline
    test_started_on TIMESTAMP,
    test_ended_on TIMESTAMP,

    -- Dimensional Checklist (3 items as per template)
    dim1_dimension TEXT, dim1_tolerance TEXT, dim1_observed_value TEXT, dim1_instrument_used TEXT, dim1_remarks TEXT, dim1_upload TEXT,
    dim2_dimension TEXT, dim2_tolerance TEXT, dim2_observed_value TEXT, dim2_instrument_used TEXT, dim2_remarks TEXT, dim2_upload TEXT,
    dim3_dimension TEXT, dim3_tolerance TEXT, dim3_observed_value TEXT, dim3_instrument_used TEXT, dim3_remarks TEXT, dim3_upload TEXT,

    -- Parameter Checklist (8 fixed parameters as per template)
    param1_name TEXT DEFAULT 'Burrs', param1_allowed TEXT, param1_yes_no VARCHAR(10), param1_expected TEXT, param1_remarks TEXT, param1_upload TEXT,
    param2_name TEXT DEFAULT 'Damages', param2_allowed TEXT, param2_yes_no VARCHAR(10), param2_expected TEXT, param2_remarks TEXT, param2_upload TEXT,
    param3_name TEXT DEFAULT 'Name Plate', param3_allowed TEXT, param3_yes_no VARCHAR(10), param3_expected TEXT, param3_remarks TEXT, param3_upload TEXT,
    param4_name TEXT DEFAULT 'Engraving', param4_allowed TEXT, param4_yes_no VARCHAR(10), param4_expected TEXT, param4_remarks TEXT, param4_upload TEXT,
    param5_name TEXT DEFAULT 'Passivation', param5_allowed TEXT, param5_yes_no VARCHAR(10), param5_expected TEXT, param5_remarks TEXT, param5_upload TEXT,
    param6_name TEXT DEFAULT 'Chromate', param6_allowed TEXT, param6_yes_no VARCHAR(10), param6_expected TEXT, param6_remarks TEXT, param6_upload TEXT,
    param7_name TEXT DEFAULT 'Electro-less Nickel plating', param7_allowed TEXT, param7_yes_no VARCHAR(10), param7_expected TEXT, param7_remarks TEXT, param7_upload TEXT,
    param8_name TEXT DEFAULT 'Fasteners', param8_allowed TEXT, param8_yes_no VARCHAR(10), param8_expected TEXT, param8_remarks TEXT, param8_upload TEXT,

    -- Signatories
    prepared_by TEXT,
    verified_by TEXT,
    approved_by TEXT,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create a function to update the updated_at column (if not exists)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 3. Create the trigger
CREATE TRIGGER trg_update_updated_at_mechanical
BEFORE UPDATE ON mechanical_inspection_report
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE mechanical_inspection_report IS 'Mechanical inspection reports based on MechanicalInspection.vue template';
COMMENT ON COLUMN mechanical_inspection_report.project_name IS 'Project name from general information';
COMMENT ON COLUMN mechanical_inspection_report.product_name IS 'Product/LRU name being inspected';
COMMENT ON COLUMN mechanical_inspection_report.dp_name IS 'DP (Design Point) name';
COMMENT ON COLUMN mechanical_inspection_report.test_started_on IS 'Test start timestamp';
COMMENT ON COLUMN mechanical_inspection_report.test_ended_on IS 'Test end timestamp';
COMMENT ON COLUMN mechanical_inspection_report.dim1_dimension IS 'First dimensional measurement - dimension';
COMMENT ON COLUMN mechanical_inspection_report.dim1_tolerance IS 'First dimensional measurement - tolerance';
COMMENT ON COLUMN mechanical_inspection_report.dim1_observed_value IS 'First dimensional measurement - observed value';
COMMENT ON COLUMN mechanical_inspection_report.dim1_instrument_used IS 'First dimensional measurement - instrument used';
COMMENT ON COLUMN mechanical_inspection_report.dim1_remarks IS 'First dimensional measurement - remarks';
COMMENT ON COLUMN mechanical_inspection_report.dim1_upload IS 'First dimensional measurement - uploaded file path';
COMMENT ON COLUMN mechanical_inspection_report.param1_name IS 'First parameter name (default: Burrs)';
COMMENT ON COLUMN mechanical_inspection_report.param1_allowed IS 'First parameter - allowed/not allowed';
COMMENT ON COLUMN mechanical_inspection_report.param1_yes_no IS 'First parameter - Yes/No selection';
COMMENT ON COLUMN mechanical_inspection_report.param1_expected IS 'First parameter - expected value';
COMMENT ON COLUMN mechanical_inspection_report.param1_remarks IS 'First parameter - remarks/observations';
COMMENT ON COLUMN mechanical_inspection_report.param1_upload IS 'First parameter - uploaded file path';
