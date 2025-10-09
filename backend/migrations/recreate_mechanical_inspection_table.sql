-- Migration: Recreate mechanical inspection report table
-- Date: 2025-01-15
-- Description: Recreates table for mechanical inspection reports based on MechanicalInspection.vue template

-- 1. Create the mechanical inspection report table
CREATE TABLE mechanical_inspection_report (
    report_id SERIAL PRIMARY KEY,

    -- Header info
    project_name TEXT,
    report_ref_no VARCHAR(100),
    memo_ref_no VARCHAR(100),
    lru_name TEXT,
    sru_name TEXT,
    dp_name TEXT,
    part_no VARCHAR(100),
    inspection_stage TEXT,
    test_venue TEXT,
    quantity INT,
    sl_nos TEXT,
    start_date DATE,
    end_date DATE,
    dated1 DATE,
    dated2 DATE,

    -- Dimensional Checklist (3 items as per template)
    dim1_dimension TEXT, dim1_tolerance TEXT, dim1_observed_value TEXT, dim1_instrument_used TEXT, dim1_remarks TEXT, dim1_upload TEXT,
    dim2_dimension TEXT, dim2_tolerance TEXT, dim2_observed_value TEXT, dim2_instrument_used TEXT, dim2_remarks TEXT, dim2_upload TEXT,
    dim3_dimension TEXT, dim3_tolerance TEXT, dim3_observed_value TEXT, dim3_instrument_used TEXT, dim3_remarks TEXT, dim3_upload TEXT,

    -- Parameter Checklist (8 fixed parameters as per template)
    param1_name TEXT DEFAULT 'Burrs', param1_compliance_observation TEXT, param1_expected TEXT DEFAULT 'Not Expected', param1_remarks TEXT, param1_upload TEXT,
    param2_name TEXT DEFAULT 'Damages', param2_compliance_observation TEXT, param2_expected TEXT DEFAULT 'Not Expected', param2_remarks TEXT, param2_upload TEXT,
    param3_name TEXT DEFAULT 'Name Plate', param3_compliance_observation TEXT, param3_expected TEXT DEFAULT 'As per Drawing', param3_remarks TEXT, param3_upload TEXT,
    param4_name TEXT DEFAULT 'Engraving', param4_compliance_observation TEXT, param4_expected TEXT DEFAULT 'As per Drawing', param4_remarks TEXT, param4_upload TEXT,
    param5_name TEXT DEFAULT 'Passivation', param5_compliance_observation TEXT, param5_expected TEXT DEFAULT 'As per Drawing', param5_remarks TEXT, param5_upload TEXT,
    param6_name TEXT DEFAULT 'Chromate', param6_compliance_observation TEXT, param6_expected TEXT DEFAULT 'As per Drawing', param6_remarks TEXT, param6_upload TEXT,
    param7_name TEXT DEFAULT 'Electro-less Nickel plating', param7_compliance_observation TEXT, param7_expected TEXT DEFAULT 'As per Drawing', param7_remarks TEXT, param7_upload TEXT,
    param8_name TEXT DEFAULT 'Fasteners', param8_compliance_observation TEXT, param8_expected TEXT DEFAULT 'As per Drawing', param8_remarks TEXT, param8_upload TEXT,

    -- Footer / Summary
    overall_status TEXT,
    quality_rating INT,
    recommendations TEXT,

    -- Signatories
    prepared_by TEXT,
    verified_by TEXT,
    approved_by TEXT,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create a function to update the updated_at column
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
COMMENT ON COLUMN mechanical_inspection_report.lru_name IS 'LRU (Line Replaceable Unit) name being inspected';
COMMENT ON COLUMN mechanical_inspection_report.dp_name IS 'DP (Design Point) name';
COMMENT ON COLUMN mechanical_inspection_report.start_date IS 'Inspection start date';
COMMENT ON COLUMN mechanical_inspection_report.end_date IS 'Inspection end date';
COMMENT ON COLUMN mechanical_inspection_report.dim1_dimension IS 'First dimensional measurement - dimension';
COMMENT ON COLUMN mechanical_inspection_report.dim1_tolerance IS 'First dimensional measurement - tolerance';
COMMENT ON COLUMN mechanical_inspection_report.dim1_observed_value IS 'First dimensional measurement - observed value';
COMMENT ON COLUMN mechanical_inspection_report.dim1_instrument_used IS 'First dimensional measurement - instrument used';
COMMENT ON COLUMN mechanical_inspection_report.dim1_remarks IS 'First dimensional measurement - remarks';
COMMENT ON COLUMN mechanical_inspection_report.dim1_upload IS 'First dimensional measurement - uploaded file path';
COMMENT ON COLUMN mechanical_inspection_report.param1_name IS 'First parameter name (default: Burrs)';
COMMENT ON COLUMN mechanical_inspection_report.param1_compliance_observation IS 'First parameter - compliance observations';
COMMENT ON COLUMN mechanical_inspection_report.param1_expected IS 'First parameter - expected value (default: Not Expected)';
COMMENT ON COLUMN mechanical_inspection_report.param1_remarks IS 'First parameter - remarks (OK/NOT OK)';
COMMENT ON COLUMN mechanical_inspection_report.param1_upload IS 'First parameter - uploaded file path';
