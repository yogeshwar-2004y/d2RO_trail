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
(1002, 'Sudhiksha M K', 'sudhikshamk06@gmail.com', 'admin'),
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




