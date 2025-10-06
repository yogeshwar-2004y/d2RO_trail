CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO roles (role_name) VALUES
('Admin'),
('QA Head'),
('QA Reviewer'),
('Design Head'),
('Designer');

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

INSERT INTO users (user_id, name, email, password_hash) VALUES
(1001, 'Avanthika PG', 'avanthikapg22@gmail.com', 'reviewer'),
(1002, 'Sudhiksha M K', 'sudhikshamk06@gmail.com', 'password'),
(1003, 'Mahadev M', 'mahadevmanohar07@gmail.com', 'designhead'),
(1004, 'Mohan', 'mohan@gmail.com', 'qahead'),
(1005, 'Mahaashri C V', 'mahaashri@gmail.com', 'designer');

CREATE TABLE IF NOT EXISTS user_roles (
    user_role_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    role_id INT NOT NULL REFERENCES roles(role_id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT now()
);

INSERT INTO user_roles (user_id, role_id) VALUES
(1001, 3),
(1002, 1),
(1003, 4),
(1004, 2),
(1005, 5);

CREATE TABLE IF NOT EXISTS projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(50) NOT NULL,
    created_by INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT now(),
    project_date DATE NOT NULL
);

INSERT INTO projects (project_name, created_by, project_date) VALUES
('Flight Control System', 1002, '2025-01-01'),
('Navigation Module', 1003, '2025-01-01');

CREATE TABLE IF NOT EXISTS lrus (
    lru_id SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    lru_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO lrus (project_id, lru_name) VALUES
(1, 'Flight Computer'),
(1, 'Autopilot System'),
(2, 'GPS Receiver'),
(2, 'Navigation Display');


CREATE TABLE IF NOT EXISTS serial_numbers (
    serial_id SERIAL PRIMARY KEY,
    lru_id INT NOT NULL REFERENCES lrus(lru_id) ON DELETE CASCADE,
    serial_number INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO serial_numbers (lru_id, serial_number) VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 1),
(4, 1);

CREATE TABLE IF NOT EXISTS plan_documents (
    document_id SERIAL PRIMARY KEY,
    lru_id INT NOT NULL REFERENCES lrus(lru_id) ON DELETE CASCADE,
    document_number VARCHAR(50) NOT NULL,
    version VARCHAR(10),
    revision VARCHAR(10),
    doc_ver VARCHAR(2) CHECK (doc_ver ~ '^[A-Z]{1,2}$'),
    uploaded_by INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    upload_date TIMESTAMP DEFAULT NOW(),
    file_path VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'not assigned' CHECK (
        status IN (
            'disapproved',
            'assigned and returned',
            'moved to next stage',
            'not cleared',
            'not assigned'
        )
    ),
    is_active BOOLEAN DEFAULT TRUE
);


INSERT INTO plan_documents (lru_id, document_number, version, revision, doc_ver, uploaded_by, file_path, status) VALUES
(1, 'DOC-FC-001', 'v1.0', 'r1', 'A', 1002, '/docs/fc/doc-fc-001-v1.0.pdf', 'not assigned'),
(2, 'DOC-AP-001', 'v1.0', 'r2', 'B', 1003, '/docs/ap/doc-ap-001-v1.0.pdf', 'assigned and returned'),
(3, 'DOC-GPS-001', 'v1.1', 'r1', 'C', 1004, '/docs/gps/doc-gps-001-v1.1.pdf', 'cleared'),
(4, 'DOC-ND-001', 'v2.0', 'r3', 'D', 1005, '/docs/nd/doc-nd-001-v2.0.pdf', 'disapproved');

CREATE TABLE IF NOT EXISTS document_version (
    version_id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES plan_documents(document_id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL,
    revision VARCHAR(20),
    doc_version VARCHAR(2) NOT NULL CHECK (doc_version ~ '^[A-Z]{1,2}$'),
    uploaded_by INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    uploaded_date TIMESTAMP DEFAULT now(),
    file_path VARCHAR(255) NOT NULL
 );

INSERT INTO document_version 
    (document_id, version, revision, doc_version, uploaded_by, file_path)
VALUES
    (6, 'v1.0', 'R1', 'A', 1001, '/files/documents/doc1_v1.pdf'),
    (6, 'v1.1', 'R2', 'B', 1002, '/files/documents/doc1_v1.1.pdf'),
    (7, 'v2.0', 'R1', 'A', 1001, '/files/documents/doc2_v2.pdf'),
    (8, 'v1.0', 'R1', 'A', 1003, '/files/documents/doc3_v1.pdf'),
    (8, 'v1.1', 'R2', 'B', 1002, '/files/documents/doc3_v1.1.pdf');

 

CREATE TABLE IF NOT EXISTS document_reviews (
    review_id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES plan_documents(document_id) ON DELETE CASCADE,
    reviewer_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
    review_date TIMESTAMP DEFAULT now()
);

INSERT INTO document_reviews (document_id, reviewer_id, status) VALUES
(6, 1001, 'pending'),
(7, 1001, 'accepted'),
(8, 1004, 'rejected'),
(9, 1005, 'pending');

CREATE TABLE IF NOT EXISTS review_comments (
    comment_id SERIAL PRIMARY KEY,
    review_id INT NOT NULL REFERENCES document_reviews(review_id) ON DELETE CASCADE,
    commented_by INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    comment_text TEXT NOT NULL,
    classification VARCHAR(10) NOT NULL CHECK (classification IN ('major', 'minor')),
    justification TEXT,
    status VARCHAR(10) DEFAULT 'open' CHECK (status IN ('open', 'resolved')),
    timestamp TIMESTAMP DEFAULT now()
);

INSERT INTO review_comments (review_id, commented_by, comment_text, classification, justification, status) VALUES
(5, 1001, 'Need clarification on section 3.2', 'major', 'Critical requirement missing', 'open'),
(5, 1002, 'Formatting issue in section 2.1', 'minor', 'Not critical but should be fixed', 'resolved'),
(6, 1003, 'Good work, approved for next stage', 'minor', NULL, 'resolved'),
(7, 1004, 'Incorrect data handling observed', 'major', 'Must be corrected before approval', 'open');


CREATE TABLE IF NOT EXISTS tests (
    test_id SERIAL PRIMARY KEY,
    test_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO tests (test_name) VALUES
('Initial Integration Test'),
('System Performance Test'),
('Navigation Accuracy Test');

CREATE TABLE IF NOT EXISTS stages (
    stage_id SERIAL PRIMARY KEY,
    stage_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO stages (stage_name) VALUES
('Design Stage'),
('Implementation Stage'),
('Testing Stage', 3),
('Deployment Stage');


CREATE TABLE IF NOT EXISTS stage_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO stage_types (type_name) VALUES
('Functional'),
('Performance'),
('Regression'),
('Acceptance');

CREATE TABLE IF NOT EXISTS test_stage_types (
    test_id INT NOT NULL REFERENCES tests(test_id) ON DELETE CASCADE,
    stage_id INT NOT NULL REFERENCES stages(stage_id) ON DELETE CASCADE,
    type_id INT NOT NULL REFERENCES stage_types(type_id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT NOW(),
    assigned_by INT REFERENCES users(user_id) ON DELETE CASCADE,
    -- ensure only one type per stage per test
    CONSTRAINT unique_test_stage UNIQUE (test_id, stage_id)
);

INSERT INTO test_stage_types (test_id, stage_id, type_id, assigned_by) VALUES
(1, 1, 1, 1002), 
(1, 2, 2, 1003), 
(2, 3, 3, 1004), 
(3, 4, 4, 1005); 


CREATE TABLE plan_doc_assignment (
    assignment_id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES plan_documents(document_id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT now(),
    UNIQUE (document_id, user_id)
);

CREATE TABLE memos (
    memo_id SERIAL PRIMARY KEY,
    from_person TEXT NOT NULL,
    to_person TEXT NOT NULL,
    thru_person TEXT,
    casdic_ref_no VARCHAR,
    dated DATE,
    wing_proj_ref_no VARCHAR,
    lru_sru_desc TEXT,
    part_number VARCHAR,
    slno_units TEXT[],               -- array of checkbox selections
    qty_offered INT,                 -- derived: count of slno_units
    manufacturer VARCHAR(255),
    drawing_no_rev TEXT,
    source TEXT,
    unit_identification TEXT[],      -- changed to array type
    mechanical_inspn TEXT,
    inspn_test_stage_offered TEXT,
    stte_status TEXT,
    test_stage_cleared TEXT,
    venue TEXT,
    memo_date DATE,
    name_designation TEXT,
    test_facility VARCHAR(255),
    test_cycle_duration TEXT,        -- changed from FLOAT to TEXT
    test_start_on TIMESTAMP,
    test_complete_on TIMESTAMP,
    calibration_status TEXT,
    func_check_initial TIMESTAMP,
    perf_check_during TIMESTAMP,
    func_check_end TIMESTAMP,
    certified TEXT[],                -- store a-f checkbox selections
    remarks TEXT,
    submitted_at TIMESTAMP,          -- new column
    submitted_by INT REFERENCES users(user_id) ON DELETE CASCADE,  -- new column
    accepted_at TIMESTAMP,           -- new column
    accepted_by INT REFERENCES users(user_id) ON DELETE CASCADE,   -- new column
    memo_status VARCHAR(20) NOT NULL DEFAULT 'not assigned'
        CHECK (memo_status IN ('assigned', 'not assigned', 'disapproved'))
);

CREATE TABLE IF NOT EXISTS news_updates (
    id SERIAL PRIMARY KEY,
    news_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    hidden BOOLEAN DEFAULT FALSE
);

CREATE TABLE memo_references (
    ref_id SERIAL PRIMARY KEY,
    memo_id INT REFERENCES memos(memo_id) ON DELETE CASCADE,
    ref_doc VARCHAR(255),
    ref_no VARCHAR(255),
    ver FLOAT,
    rev FLOAT
);

CREATE TABLE reports (
    report_id SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    lru_id INT NOT NULL REFERENCES lrus(lru_id) ON DELETE CASCADE,
    serial_id INT NOT NULL REFERENCES serial_numbers(serial_id) ON DELETE CASCADE,
    inspection_stage TEXT,
    date_of_review DATE,
    review_venue TEXT,
    reference_document INT REFERENCES plan_documents(document_id) ON DELETE SET NULL
);


CREATE TABLE report_observations (
    obs_id SERIAL PRIMARY KEY,
    report_id INT NOT NULL REFERENCES reports(report_id) ON DELETE CASCADE,
    s_no INT NOT NULL,
    category VARCHAR(10) CHECK (category IN ('major', 'minor')),
    observation TEXT NOT NULL
);

CREATE TABLE memo_approval (
    approval_id SERIAL PRIMARY KEY,
    memo_id INT NOT NULL UNIQUE REFERENCES memos(memo_id) ON DELETE CASCADE,
    test_date DATE,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    comments TEXT,
    authentication TEXT,
    attachment_path TEXT,
    status VARCHAR(10) NOT NULL CHECK (status IN ('accepted', 'rejected')),
    approval_date TIMESTAMP DEFAULT NOW(),
    approved_by INT REFERENCES users(user_id)
);


CREATE TABLE project_users (
    project_user_id SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT now(),
    CONSTRAINT unique_project_user UNIQUE (project_id, user_id)
);

CREATE TABLE shared_memos (
    share_id SERIAL PRIMARY KEY,
    memo_id INT NOT NULL REFERENCES memos(memo_id) ON DELETE CASCADE,
    shared_by INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    shared_with INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    shared_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_not_self_share CHECK (shared_by <> shared_with)
);

CREATE TABLE report_templates ( 
    template_id SERIAL PRIMARY KEY, 
    template_name VARCHAR(50) NOT NULL
);

INSERT INTO report_templates (template_name) 
VALUES
('conformal coating inspection report'),
('cots screening inspection report'),
('bare pcb inspection report'),
('mechanical inspection report'),
('assembled board inspection report'), 
('raw material inspection report'),
('kit of part inspection report');

-- 1. Create the table
CREATE TABLE bare_pcb_inspection_report (
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
    serial_number VARCHAR(100),
    inspection_count VARCHAR(50),
    start_date DATE,
    end_date DATE,
    dated1 DATE,
    dated2 DATE,

    -- Parameters (12 fixed checklist items)
    obs1 TEXT,  rem1 VARCHAR(20),  upload1 TEXT,
    obs2 TEXT,  rem2 VARCHAR(20),  upload2 TEXT,
    obs3 TEXT,  rem3 VARCHAR(20),  upload3 TEXT,
    obs4 TEXT,  rem4 VARCHAR(20),  upload4 TEXT,
    obs5 TEXT,  rem5 VARCHAR(20),  upload5 TEXT,
    obs6 TEXT,  rem6 VARCHAR(20),  upload6 TEXT,
    obs7 TEXT,  rem7 VARCHAR(20),  upload7 TEXT,
    obs8 TEXT,  rem8 VARCHAR(20),  upload8 TEXT,
    obs9 TEXT,  rem9 VARCHAR(20),  upload9 TEXT,
    obs10 TEXT, rem10 VARCHAR(20), upload10 TEXT,
    obs11 TEXT, rem11 VARCHAR(20), upload11 TEXT,
    obs12 TEXT, rem12 VARCHAR(20), upload12 TEXT,

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
CREATE TRIGGER trg_update_updated_at
BEFORE UPDATE ON bare_pcb_inspection_report
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE TABLE assembled_board_inspection_report (
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
    serial_number VARCHAR(100),
    start_date DATE,
    end_date DATE,
    dated1 DATE,
    dated2 DATE,

    -- 20 Parameters (Observation, Remarks, Upload)
    obs1 TEXT,  rem1 VARCHAR(20) CHECK (rem1 IN ('OK','NOT OK')),  upload1 TEXT,
    obs2 TEXT,  rem2 VARCHAR(20) CHECK (rem2 IN ('OK','NOT OK')),  upload2 TEXT,
    obs3 TEXT,  rem3 VARCHAR(20) CHECK (rem3 IN ('OK','NOT OK')),  upload3 TEXT,
    obs4 TEXT,  rem4 VARCHAR(20) CHECK (rem4 IN ('OK','NOT OK')),  upload4 TEXT,
    obs5 TEXT,  rem5 VARCHAR(20) CHECK (rem5 IN ('OK','NOT OK')),  upload5 TEXT,
    obs6 TEXT,  rem6 VARCHAR(20) CHECK (rem6 IN ('OK','NOT OK')),  upload6 TEXT,
    obs7 TEXT,  rem7 VARCHAR(20) CHECK (rem7 IN ('OK','NOT OK')),  upload7 TEXT,
    obs8 TEXT,  rem8 VARCHAR(20) CHECK (rem8 IN ('OK','NOT OK')),  upload8 TEXT,
    obs9 TEXT,  rem9 VARCHAR(20) CHECK (rem9 IN ('OK','NOT OK')),  upload9 TEXT,
    obs10 TEXT, rem10 VARCHAR(20) CHECK (rem10 IN ('OK','NOT OK')), upload10 TEXT,
    obs11 TEXT, rem11 VARCHAR(20) CHECK (rem11 IN ('OK','NOT OK')), upload11 TEXT,
    obs12 TEXT, rem12 VARCHAR(20) CHECK (rem12 IN ('OK','NOT OK')), upload12 TEXT,
    obs13 TEXT, rem13 VARCHAR(20) CHECK (rem13 IN ('OK','NOT OK')), upload13 TEXT,
    obs14 TEXT, rem14 VARCHAR(20) CHECK (rem14 IN ('OK','NOT OK')), upload14 TEXT,
    obs15 TEXT, rem15 VARCHAR(20) CHECK (rem15 IN ('OK','NOT OK')), upload15 TEXT,
    obs16 TEXT, rem16 VARCHAR(20) CHECK (rem16 IN ('OK','NOT OK')), upload16 TEXT,
    obs17 TEXT, rem17 VARCHAR(20) CHECK (rem17 IN ('OK','NOT OK')), upload17 TEXT,
    obs18 TEXT, rem18 VARCHAR(20) CHECK (rem18 IN ('OK','NOT OK')), upload18 TEXT,
    obs19 TEXT, rem19 VARCHAR(20) CHECK (rem19 IN ('OK','NOT OK')), upload19 TEXT,
    obs20 TEXT, rem20 VARCHAR(20) CHECK (rem20 IN ('OK','NOT OK')), upload20 TEXT,

    -- Signatories
    prepared_by TEXT,
    verified_by TEXT,
    approved_by TEXT,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Auto-update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_updated_at
BEFORE UPDATE ON assembled_board_inspection_report
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE cot_screening_inspection_report (
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
    serial_number VARCHAR(100),
    start_date DATE,
    end_date DATE,
    dated1 DATE,
    dated2 DATE,

    -- Checklist parameters
    rem1 VARCHAR(20) CHECK (rem1 IN ('OK','NOT OK')), upload1 TEXT,
    rem2 VARCHAR(20) CHECK (rem2 IN ('OK','NOT OK')), upload2 TEXT,

    -- Signatories
    prepared_by TEXT,
    verified_by TEXT,
    approved_by TEXT,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_updated_at
BEFORE UPDATE ON cot_screening_inspection_report
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

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


-- 1. Create the kit of parts inspection report table
CREATE TABLE kit_of_parts_inspection_report (
    report_id SERIAL PRIMARY KEY,

    -- Header info (from General Information section)
    project_name TEXT,
    dp_name TEXT,
    report_ref_no VARCHAR(100),
    memo_ref_no VARCHAR(100),
    lru_name TEXT,
    sru_name TEXT,
    part_no VARCHAR(100),
    quantity INT,
    sl_nos TEXT,
    test_venue TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,

    -- Inspection Results (7 fixed test cases as per template)
    test1_sl_no INT DEFAULT 1,
    test1_case TEXT DEFAULT 'Any observation pending from previous KOP stage',
    test1_expected TEXT DEFAULT 'NIL',
    test1_observations TEXT,
    test1_remarks VARCHAR(10) CHECK (test1_remarks IN ('OK', 'NOT OK', '')),
    test1_upload TEXT,

    test2_sl_no INT DEFAULT 2,
    test2_case TEXT DEFAULT 'CoC verification of components',
    test2_expected TEXT DEFAULT 'Verified',
    test2_observations TEXT,
    test2_remarks VARCHAR(10) CHECK (test2_remarks IN ('OK', 'NOT OK', '')),
    test2_upload TEXT,

    test3_sl_no INT DEFAULT 3,
    test3_case TEXT DEFAULT 'Quantity as BOM',
    test3_expected TEXT DEFAULT 'Matching',
    test3_observations TEXT,
    test3_remarks VARCHAR(10) CHECK (test3_remarks IN ('OK', 'NOT OK', '')),
    test3_upload TEXT,

    test4_sl_no INT DEFAULT 4,
    test4_case TEXT DEFAULT 'Quantity as per number of boards to be assembled',
    test4_expected TEXT DEFAULT 'Matching',
    test4_observations TEXT,
    test4_remarks VARCHAR(10) CHECK (test4_remarks IN ('OK', 'NOT OK', '')),
    test4_upload TEXT,

    test5_sl_no INT DEFAULT 5,
    test5_case TEXT DEFAULT 'Components storage in ESD cover',
    test5_expected TEXT DEFAULT 'Stored in ESD',
    test5_observations TEXT,
    test5_remarks VARCHAR(10) CHECK (test5_remarks IN ('OK', 'NOT OK', '')),
    test5_upload TEXT,

    test6_sl_no INT DEFAULT 6,
    test6_case TEXT DEFAULT 'All connectors to be fitted with screws before assembly',
    test6_expected TEXT DEFAULT 'Fitted properly',
    test6_observations TEXT,
    test6_remarks VARCHAR(10) CHECK (test6_remarks IN ('OK', 'NOT OK', '')),
    test6_upload TEXT,

    test7_sl_no INT DEFAULT 7,
    test7_case TEXT DEFAULT 'Any other observations',
    test7_expected TEXT DEFAULT 'NIL',
    test7_observations TEXT,
    test7_remarks VARCHAR(10) CHECK (test7_remarks IN ('OK', 'NOT OK', '')),
    test7_upload TEXT,

    -- Signatories (specific roles as per template)
    prepared_by_qa_g1 TEXT,
    verified_by_g1h_qa_g TEXT,
    approved_by TEXT,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create a function to update the updated_at column (reuse existing function)
-- Note: The function update_updated_at_column() should already exist from previous tables

-- 3. Create the trigger
CREATE TRIGGER trg_update_updated_at_kit_of_parts
BEFORE UPDATE ON kit_of_parts_inspection_report
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();