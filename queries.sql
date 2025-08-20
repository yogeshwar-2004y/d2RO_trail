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

CREATE TABLE IF NOT EXISTS serial_numbers (
    serial_id SERIAL PRIMARY KEY,
    lru_id INT NOT NULL REFERENCES lrus(lru_id),
    serial_number VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS plan_documents (
    document_id SERIAL PRIMARY KEY,
    lru_id INT NOT NULL REFERENCES lrus(lru_id),
    document_number VARCHAR(50) NOT NULL,
    version VARCHAR(10),
    revision VARCHAR(10),
    doc_ver CHAR(2) CHECK (doc_ver ~ '^[A-Z]{1,2}$'),
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

CREATE TABLE IF NOT EXISTS document_version (
    version_id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES plan_documents(document_id),
    version VARCHAR(20) NOT NULL,
    revision VARCHAR(20),
    doc_version CHAR(2) NOT NULL CHECK (doc_version ~ '^[A-Z]{1,2}$'),
    uploaded_by INT NOT NULL REFERENCES users(user_id),
    uploaded_date TIMESTAMP DEFAULT now(),
    file_path VARCHAR(255) NOT NULL
 );

CREATE TABLE IF NOT EXISTS document_reviews (
    review_id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES plan_documents(document_id),
    reviewer_id INT NOT NULL REFERENCES users(user_id),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
    review_date TIMESTAMP DEFAULT now()
);

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

CREATE TABLE IF NOT EXISTS tests (
    test_id SERIAL PRIMARY KEY,
    test_code VARCHAR(20) NOT NULL UNIQUE,
    test_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stages (
    stage_id SERIAL PRIMARY KEY,
    stage_name VARCHAR(50) NOT NULL UNIQUE,
    stage_order INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stage_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS test_stage_types (
    test_id INT NOT NULL REFERENCES tests(test_id),
    stage_id INT NOT NULL REFERENCES stages(stage_id),
    type_id INT NOT NULL REFERENCES stage_types(type_id),
    assigned_at TIMESTAMP DEFAULT NOW(),
    assigned_by INT REFERENCES users(user_id),
    -- ensure only one type per stage per test
    CONSTRAINT unique_test_stage UNIQUE (test_id, stage_id)
);

