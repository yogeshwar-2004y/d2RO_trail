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
    user_id INT NOT NULL REFERENCES users(user_id),
    role_id INT NOT NULL REFERENCES roles(role_id),
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
    description TEXT,
    created_by INT NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT now()
);

INSERT INTO projects (project_name, description, created_by) VALUES
('Flight Control System', 'Software for controlling flight systems', 1002),
('Navigation Module', 'Module for handling GPS and navigation', 1003);

CREATE TABLE IF NOT EXISTS lrus (
    lru_id SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES projects(project_id),
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
    lru_id INT NOT NULL REFERENCES lrus(lru_id),
    serial_number VARCHAR(50) NOT NULL,
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
    lru_id INT NOT NULL REFERENCES lrus(lru_id),
    document_number VARCHAR(50) NOT NULL,
    version VARCHAR(10),
    revision VARCHAR(10),
    doc_ver VARCHAR(2) CHECK (doc_ver ~ '^[A-Z]{1,2}$'),
    uploaded_by INT NOT NULL REFERENCES users(user_id),
    upload_date TIMESTAMP DEFAULT NOW(),
    file_path VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'not assigned' CHECK (
        status IN (
            'cleared',
            'disapproved',
            'assigned and returned',
            'moved to next stage',
            'not cleared',
            'not assigned'
        )
    ),
    is_active BOOLEAN DEFAULT TRUE
);


INSERT INTO plan_documents (lru_id, document_number, vers, revision, doc_ver, uploaded_by, file_path, status) VALUES
(1, 'DOC-FC-001', 'v1.0', 'r1', 'A', 1002, '/docs/fc/doc-fc-001-v1.0.pdf', 'not assigned'),
(2, 'DOC-AP-001', 'v1.0', 'r2', 'B', 1003, '/docs/ap/doc-ap-001-v1.0.pdf', 'assigned and returned'),
(3, 'DOC-GPS-001', 'v1.1', 'r1', 'C', 1004, '/docs/gps/doc-gps-001-v1.1.pdf', 'cleared'),
(4, 'DOC-ND-001', 'v2.0', 'r3', 'D', 1005, '/docs/nd/doc-nd-001-v2.0.pdf', 'disapproved');

CREATE TABLE IF NOT EXISTS document_version (
    version_id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES plan_documents(document_id),
    version VARCHAR(20) NOT NULL,
    revision VARCHAR(20),
    doc_version VARCHAR(2) NOT NULL CHECK (doc_version ~ '^[A-Z]{1,2}$'),
    uploaded_by INT NOT NULL REFERENCES users(user_id),
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
    document_id INT NOT NULL REFERENCES plan_documents(document_id),
    reviewer_id INT NOT NULL REFERENCES users(user_id),
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
    review_id INT NOT NULL REFERENCES document_reviews(review_id),
    commented_by INT NOT NULL REFERENCES users(user_id),
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
    test_code VARCHAR(20) NOT NULL UNIQUE,
    test_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO tests (test_code, test_name) VALUES
('TST-001', 'Initial Integration Test'),
('TST-002', 'System Performance Test'),
('TST-003', 'Navigation Accuracy Test');

CREATE TABLE IF NOT EXISTS stages (
    stage_id SERIAL PRIMARY KEY,
    stage_name VARCHAR(50) NOT NULL UNIQUE,
    stage_order INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO stages (stage_name, stage_order) VALUES
('Design Stage', 1),
('Implementation Stage', 2),
('Testing Stage', 3),
('Deployment Stage', 4);


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
    test_id INT NOT NULL REFERENCES tests(test_id),
    stage_id INT NOT NULL REFERENCES stages(stage_id),
    type_id INT NOT NULL REFERENCES stage_types(type_id),
    assigned_at TIMESTAMP DEFAULT NOW(),
    assigned_by INT REFERENCES users(user_id),
    -- ensure only one type per stage per test
    CONSTRAINT unique_test_stage UNIQUE (test_id, stage_id)
);

INSERT INTO test_stage_types (test_id, stage_id, type_id, assigned_by) VALUES
(1, 1, 1, 1002), -- Design stage functional test
(1, 2, 2, 1003), -- Implementation stage performance test
(2, 3, 3, 1004), -- Testing stage regression test
(3, 4, 4, 1005); -- Deployment stage acceptance test
