from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import psycopg2
import hashlib
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
CORS(app, origins="*", supports_credentials=True)


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return hash_password(password) == hashed_password

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="ERP",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

# @app.after_request
# def after_request(response):
#     response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
#     response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
#     response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
#     return response


@app.route('/api')
def hello_world():
    return jsonify(message="Hello from Flask!")

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        cur = conn.cursor()
        
        # Join users, user_roles, and roles tables to get proper role information
        cur.execute("""
            SELECT u.user_id, u.name, u.email, u.password_hash, r.role_id, r.role_name
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            WHERE u.email = %s
        """, (email,))
        
        user = cur.fetchone()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 401

        # Check if password matches (password_hash column stores plain text passwords)
        if verify_password(password, user[3]):
            cur.close()
            return jsonify({
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "role_id": user[4],  # role_id from roles table
                    "role": user[5]  # role_name from roles table
                }
            })
        else:
            cur.close()
            print(f"Invalid password for user {email} with password as {password}")
            return jsonify({"success": False, "message": "Invalid password"}), 401
            
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Projects endpoint
@app.route('/api/projects', methods=['GET'])
def get_projects():
    print("GET /api/projects hit")  # ✅ Confirm in terminal
    try:
        cur = conn.cursor()
        
        # Fetch all projects from the projects table
        cur.execute("""
            SELECT project_id, project_name, created_at
            FROM projects
            ORDER BY project_id
        """)
        
        projects = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        project_list = []
        for project in projects:
            project_list.append({
                "id": project[0],
                "name": project[1],
                "created_at": project[2].isoformat() if project[2] else None
            })
        
        return jsonify({
            "success": True,
            "projects": project_list
        })
        
    except Exception as e:
        print(f"Error fetching projects: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# LRUs endpoint for a specific project
@app.route('/api/projects/<int:project_id>/lrus', methods=['GET'])
def get_project_lrus(project_id):
    try:
        cur = conn.cursor()
        
        # First verify the project exists
        cur.execute("""
            SELECT project_id, project_name
            FROM projects
            WHERE project_id = %s
        """, (project_id,))
        
        project = cur.fetchone()
        if not project:
            cur.close()
            return jsonify({"success": False, "message": "Project not found"}), 404
        
        # Fetch LRUs for the specific project
        cur.execute("""
            SELECT l.lru_id, l.lru_name, l.created_at
            FROM lrus l
            WHERE l.project_id = %s
            ORDER BY l.lru_id
        """, (project_id,))
        
        lrus = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        lru_list = []
        for lru in lrus:
            lru_list.append({
                "id": lru[0],
                "name": lru[1],
                "created_at": lru[2].isoformat() if lru[2] else None
            })
        
        return jsonify({
            "success": True,
            "project": {
                "id": project[0],
                "name": project[1]
            },
            "lrus": lru_list
        })
        
    except Exception as e:
        print(f"Error fetching LRUs for project {project_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Create project endpoint
@app.route('/api/projects', methods=['POST'])
def create_project():
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        project_name = data.get('name')
        project_number = data.get('number')
        project_date = data.get('date')
        lrus = data.get('lrus', [])
        created_by = data.get('createdBy')
        
        if not project_name or not project_number or not project_date:
            return jsonify({"success": False, "message": "Project name, number, and date are required"}), 400
        
        if not created_by:
            return jsonify({"success": False, "message": "User authentication required"}), 400
        
        if not lrus or len(lrus) == 0:
            return jsonify({"success": False, "message": "At least one LRU is required"}), 400
        
        # Validate LRUs and serial quantities
        for i, lru in enumerate(lrus):
            if not lru.get('name'):
                return jsonify({"success": False, "message": f"LRU {i+1} name is required"}), 400
            
            serial_quantity = lru.get('serialQuantity')
            if not serial_quantity or not isinstance(serial_quantity, int) or serial_quantity < 1:
                return jsonify({"success": False, "message": f"Valid serial quantity is required for LRU '{lru['name']}'"}), 400
        
        cur = conn.cursor()
        
        # Insert project data as specified
        cur.execute("""
            INSERT INTO projects (project_name, project_id, project_date, created_by)
            VALUES (%s, %s, %s, %s)
            RETURNING project_id
        """, (project_name, project_number, project_date, created_by))
        
        project_id = cur.fetchone()[0]
        
        # Insert LRUs with project number as project_id
        for lru in lrus:
            # Insert LRU with project number as project_id
            cur.execute("""
                INSERT INTO lrus (project_id, lru_name)
                VALUES (%s, %s)
                RETURNING lru_id
            """, (project_number, lru['name']))
            
            lru_id = cur.fetchone()[0]
            
            # Insert multiple serial numbers based on quantity
            serial_quantity = lru['serialQuantity']
            for i in range(1, serial_quantity + 1):
                cur.execute("""
                    INSERT INTO serial_numbers (lru_id, serial_number)
                    VALUES (%s, %s)
                """, (lru_id, i))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Project created successfully",
            "project_id": project_id
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error creating project: {str(e)}")
        print(f"Project data received: {data}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Update project endpoint
@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        cur = conn.cursor()
        
        # Check if project exists
        cur.execute("SELECT project_id, project_name FROM projects WHERE project_id = %s", (project_id,))
        existing_project = cur.fetchone()
        
        if not existing_project:
            cur.close()
            return jsonify({"success": False, "message": "Project not found"}), 404
        
        # Update project basic info
        update_fields = []
        update_values = []
        
        if 'name' in data and data['name']:
            update_fields.append("project_name = %s")
            update_values.append(data['name'])
            
        if 'date' in data and data['date']:
            update_fields.append("project_date = %s")
            update_values.append(data['date'])
        
        # Update project table if there are fields to update
        if update_fields:
            update_values.append(project_id)
            update_query = f"UPDATE projects SET {', '.join(update_fields)} WHERE project_id = %s"
            cur.execute(update_query, update_values)
        
        # Handle LRUs updates
        if 'lrus' in data:
            existing_lru_ids = []
            
            # Process each LRU
            for lru_data in data['lrus']:
                if 'lru_id' in lru_data and lru_data['lru_id']:
                    # Update existing LRU
                    lru_id = lru_data['lru_id']
                    existing_lru_ids.append(lru_id)
                    
                    if 'lru_name' in lru_data:
                        cur.execute("""
                            UPDATE lrus SET lru_name = %s WHERE lru_id = %s
                        """, (lru_data['lru_name'], lru_id))
                        
                else:
                    # Create new LRU
                    if lru_data.get('lru_name') and lru_data.get('serialQuantity'):
                        cur.execute("""
                            INSERT INTO lrus (project_id, lru_name)
                            VALUES (%s, %s)
                            RETURNING lru_id
                        """, (project_id, lru_data['lru_name']))
                        
                        new_lru_id = cur.fetchone()[0]
                        existing_lru_ids.append(new_lru_id)
                        
                        # Add serial numbers for new LRU
                        serial_quantity = lru_data['serialQuantity']
                        for i in range(1, serial_quantity + 1):
                            cur.execute("""
                                INSERT INTO serial_numbers (lru_id, serial_number)
                                VALUES (%s, %s)
                            """, (new_lru_id, i))
            
            # Remove LRUs that are no longer in the list (if any were removed)
            if existing_lru_ids:
                placeholders = ','.join(['%s'] * len(existing_lru_ids))
                cur.execute(f"""
                    DELETE FROM serial_numbers 
                    WHERE lru_id IN (
                        SELECT lru_id FROM lrus 
                        WHERE project_id = %s AND lru_id NOT IN ({placeholders})
                    )
                """, [project_id] + existing_lru_ids)
                
                cur.execute(f"""
                    DELETE FROM lrus 
                    WHERE project_id = %s AND lru_id NOT IN ({placeholders})
                """, [project_id] + existing_lru_ids)
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Project updated successfully"
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating project: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Get single project endpoint
@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    try:
        cur = conn.cursor()
        
        # Fetch project with LRUs and serial numbers
        cur.execute("""
            SELECT 
                p.project_id,
                p.project_name,
                p.project_date,
                p.created_at,
                l.lru_id,
                l.lru_name,
                s.serial_id,
                s.serial_number
            FROM projects p
            LEFT JOIN lrus l ON p.project_id = l.project_id
            LEFT JOIN serial_numbers s ON l.lru_id = s.lru_id
            WHERE p.project_id = %s
            ORDER BY l.lru_id, s.serial_number
        """, (project_id,))
        
        results = cur.fetchall()
        cur.close()
        
        if not results or not results[0][0]:
            return jsonify({"success": False, "message": "Project not found"}), 404
        
        # Organize data
        project_info = {
            "project_id": results[0][0],
            "project_name": results[0][1],
            "project_date": results[0][2].isoformat() if results[0][2] else None,
            "created_at": results[0][3].isoformat() if results[0][3] else None,
            "lrus": {}
        }
        
        for row in results:
            if row[4]:  # lru_id exists
                lru_id = row[4]
                if lru_id not in project_info["lrus"]:
                    project_info["lrus"][lru_id] = {
                        "lru_id": lru_id,
                        "lru_name": row[5],
                        "serial_numbers": []
                    }
                
                if row[6]:  # serial_id exists
                    project_info["lrus"][lru_id]["serial_numbers"].append({
                        "serial_id": row[6],
                        "serial_number": row[7]
                    })
        
        # Convert lrus dict to list
        project_info["lrus"] = list(project_info["lrus"].values())
        
        return jsonify({
            "success": True,
            "project": project_info
        })
        
    except Exception as e:
        print(f"Error fetching project: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Get roles endpoint
@app.route('/api/roles', methods=['GET'])
def get_roles():
    try:
        cur = conn.cursor()
        
        # Fetch all roles from the roles table
        cur.execute("""
            SELECT role_id, role_name
            FROM roles
            ORDER BY role_name
        """)
        
        roles = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        role_list = []
        for role in roles:
            role_list.append({
                "id": role[0],
                "name": role[1]
            })
        
        return jsonify({
            "success": True,
            "roles": role_list
        })
        
    except Exception as e:
        print(f"Error fetching roles: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Create user endpoint
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        user_name = data.get('name')
        user_id = data.get('id')
        email = data.get('email')
        password = data.get('password')
        role_id = data.get('roleId')
        
        if not user_name or not user_id or not email or not password or not role_id:
            return jsonify({"success": False, "message": "All fields are required"}), 400
        
        cur = conn.cursor()
        
        # Check if user_id or email already exists
        cur.execute("""
            SELECT user_id FROM users WHERE user_id = %s OR email = %s
        """, (user_id, email))
        
        existing_user = cur.fetchone()
        if existing_user:
            cur.close()
            return jsonify({"success": False, "message": "User ID or email already exists"}), 400
        
        # Hash the password
        hashed_password = hash_password(password)
        
        # Insert user into users table
        cur.execute("""
            INSERT INTO users (user_id, name, email, password_hash)
            VALUES (%s, %s, %s, %s)
        """, (user_id, user_name, email, hashed_password))
        
        # Insert role assignment into user_roles table
        cur.execute("""
            INSERT INTO user_roles (user_id, role_id)
            VALUES (%s, %s)
        """, (user_id, role_id))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "User created successfully"
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error creating user: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Update user endpoint
@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT user_id, name, email FROM users WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()
        
        if not existing_user:
            cur.close()
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Build dynamic update query based on provided fields
        update_fields = []
        update_values = []
        
        # Update user table fields
        if 'name' in data:
            update_fields.append("name = %s")
            update_values.append(data['name'])
            
        if 'email' in data:
            # Check if email is already taken by another user
            cur.execute("SELECT user_id FROM users WHERE email = %s AND user_id != %s", (data['email'], user_id))
            if cur.fetchone():
                cur.close()
                return jsonify({"success": False, "message": "Email already exists for another user"}), 400
            update_fields.append("email = %s")
            update_values.append(data['email'])
            
        if 'password' in data and data['password']:
            hashed_password = hash_password(data['password'])
            update_fields.append("password_hash = %s")
            update_values.append(hashed_password)
        
        # Update users table if there are fields to update
        if update_fields:
            update_fields.append("updated_at = NOW()")
            update_values.append(user_id)
            
            update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = %s"
            cur.execute(update_query, update_values)
        
        # Update role if provided
        if 'roleId' in data:
            # First, delete existing role assignment
            cur.execute("DELETE FROM user_roles WHERE user_id = %s", (user_id,))
            
            # Then insert new role assignment
            cur.execute("""
                INSERT INTO user_roles (user_id, role_id)
                VALUES (%s, %s)
            """, (user_id, data['roleId']))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "User updated successfully"
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating user: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Get single user endpoint
@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        cur = conn.cursor()
        
        # Fetch user with role information
        cur.execute("""
            SELECT 
                u.user_id,
                u.name,
                u.email,
                r.role_id,
                r.role_name
            FROM users u
            LEFT JOIN user_roles ur ON u.user_id = ur.user_id
            LEFT JOIN roles r ON ur.role_id = r.role_id
            WHERE u.user_id = %s
        """, (user_id,))
        
        user = cur.fetchone()
        cur.close()
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "user": {
                "user_id": user[0],
                "name": user[1],
                "email": user[2],
                "role_id": user[3],
                "role_name": user[4] if user[4] else "No Role Assigned"
            }
        })
        
    except Exception as e:
        print(f"Error fetching user: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Get projects with LRUs and serial numbers endpoint
@app.route('/api/projects/manage', methods=['GET'])
def get_projects_with_details():
    try:
        cur = conn.cursor()
        
        # Fetch all projects with their LRUs and serial numbers
        cur.execute("""
            SELECT 
                p.project_id,
                p.project_name,
                l.lru_id,
                l.lru_name,
                s.serial_id,
                s.serial_number
            FROM projects p
            LEFT JOIN lrus l ON p.project_id = l.project_id
            LEFT JOIN serial_numbers s ON l.lru_id = s.lru_id
            ORDER BY p.project_id, l.lru_id, s.serial_number
        """)
        
        results = cur.fetchall()
        cur.close()
        
        # Organize data hierarchically
        projects_dict = {}
        
        for row in results:
            project_id = row[0]
            project_name = row[1]
            lru_id = row[2]
            lru_name = row[3]
            serial_id = row[4]
            serial_number = row[5]
            
            # Initialize project if not exists
            if project_id not in projects_dict:
                projects_dict[project_id] = {
                    "project_id": project_id,
                    "project_name": project_name,
                    "lrus": {}
                }
            
            # Add LRU if it exists and not already added
            if lru_id and lru_id not in projects_dict[project_id]["lrus"]:
                projects_dict[project_id]["lrus"][lru_id] = {
                    "lru_id": lru_id,
                    "lru_name": lru_name,
                    "serial_numbers": []
                }
            
            # Add serial number if it exists
            if serial_id and lru_id:
                projects_dict[project_id]["lrus"][lru_id]["serial_numbers"].append({
                    "serial_id": serial_id,
                    "serial_number": serial_number
                })
        
        # Convert to list format for frontend
        projects_list = []
        for project_id, project_data in projects_dict.items():
            project = {
                "project_id": project_data["project_id"],
                "project_name": project_data["project_name"],
                "lrus": list(project_data["lrus"].values())
            }
            projects_list.append(project)
        
        return jsonify({
            "success": True,
            "projects": projects_list
        })
        
    except Exception as e:
        print(f"Error fetching projects with details: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Get users with roles endpoint
@app.route('/api/users/manage', methods=['GET'])
def get_users_with_roles():
    try:
        cur = conn.cursor()
        
        # Fetch all users with their roles using JOIN
        cur.execute("""
            SELECT 
                u.user_id,
                u.name,
                u.email,
                r.role_name
            FROM users u
            LEFT JOIN user_roles ur ON u.user_id = ur.user_id
            LEFT JOIN roles r ON ur.role_id = r.role_id
            ORDER BY u.user_id
        """)
        
        results = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        users_list = []
        for row in results:
            users_list.append({
                "user_id": row[0],
                "name": row[1],
                "email": row[2],
                "role": row[3] if row[3] else "No Role Assigned"
            })
        
        return jsonify({
            "success": True,
            "users": users_list
        })
        
    except Exception as e:
        print(f"Error fetching users with roles: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Plan Documents endpoints

# Get plan documents for a specific LRU
@app.route('/api/lrus/<int:lru_id>/plan-documents', methods=['GET'])
def get_lru_plan_documents(lru_id):
    try:
        cur = conn.cursor()
        
        # First verify the LRU exists
        cur.execute("""
            SELECT l.lru_id, l.lru_name, p.project_name
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            WHERE l.lru_id = %s
        """, (lru_id,))
        
        lru = cur.fetchone()
        if not lru:
            cur.close()
            return jsonify({"success": False, "message": "LRU not found"}), 404
        
        # Fetch plan documents for the specific LRU
        cur.execute("""
            SELECT 
                pd.document_id,
                pd.document_number,
                pd.version,
                pd.revision,
                pd.doc_ver,
                pd.uploaded_by,
                pd.upload_date,
                pd.file_path,
                pd.status,
                pd.original_filename,
                u.name as uploaded_by_name
            FROM plan_documents pd
            JOIN users u ON pd.uploaded_by = u.user_id
            WHERE pd.lru_id = %s AND pd.is_active = TRUE
            ORDER BY pd.document_id DESC
        """, (lru_id,))
        
        documents = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        document_list = []
        for doc in documents:
            document_list.append({
                "document_id": doc[0],
                "document_number": doc[1],
                "version": doc[2],
                "revision": doc[3],
                "doc_ver": doc[4],
                "uploaded_by": doc[5],
                "uploaded_by_name": doc[10],
                "upload_date": doc[6].isoformat() if doc[6] else None,
                "file_path": doc[7],
                "status": doc[8],
                "original_filename": doc[9]
            })
        
        return jsonify({
            "success": True,
            "lru": {
                "lru_id": lru[0],
                "lru_name": lru[1],
                "project_name": lru[2]
            },
            "documents": document_list
        })
        
    except Exception as e:
        print(f"Error fetching plan documents for LRU {lru_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Get plan documents for a project (all LRUs)
@app.route('/api/projects/<int:project_id>/plan-documents', methods=['GET'])
def get_project_plan_documents(project_id):
    try:
        cur = conn.cursor()
        
        # First verify the project exists
        cur.execute("""
            SELECT project_id, project_name
            FROM projects
            WHERE project_id = %s
        """, (project_id,))
        
        project = cur.fetchone()
        if not project:
            cur.close()
            return jsonify({"success": False, "message": "Project not found"}), 404
        
        # Fetch plan documents for all LRUs in the project
        cur.execute("""
            SELECT 
                l.lru_id,
                l.lru_name,
                pd.document_id,
                pd.document_number,
                pd.version,
                pd.revision,
                pd.doc_ver,
                pd.uploaded_by,
                pd.upload_date,
                pd.file_path,
                pd.status,
                u.name as uploaded_by_name
            FROM lrus l
            LEFT JOIN plan_documents pd ON l.lru_id = pd.lru_id AND pd.is_active = TRUE
            LEFT JOIN users u ON pd.uploaded_by = u.user_id
            WHERE l.project_id = %s
            ORDER BY l.lru_id, pd.document_id DESC
        """, (project_id,))
        
        results = cur.fetchall()
        cur.close()
        
        # Organize data by LRU
        lrus_dict = {}
        
        for row in results:
            lru_id = row[0]
            lru_name = row[1]
            
            # Initialize LRU if not exists
            if lru_id not in lrus_dict:
                lrus_dict[lru_id] = {
                    "lru_id": lru_id,
                    "lru_name": lru_name,
                    "documents": []
                }
            
            # Add document if it exists
            if row[2]:  # document_id exists
                lrus_dict[lru_id]["documents"].append({
                    "document_id": row[2],
                    "document_number": row[3],
                    "version": row[4],
                    "revision": row[5],
                    "doc_ver": row[6],
                    "uploaded_by": row[7],
                    "uploaded_by_name": row[11],
                    "upload_date": row[8].isoformat() if row[8] else None,
                    "file_path": row[9],
                    "status": row[10]
                })
        
        return jsonify({
            "success": True,
            "project": {
                "project_id": project[0],
                "project_name": project[1]
            },
            "lrus": list(lrus_dict.values())
        })
        
    except Exception as e:
        print(f"Error fetching plan documents for project {project_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Upload plan document
@app.route('/api/plan-documents', methods=['POST'])
def upload_plan_document():
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        # Get form data
        lru_id = request.form.get('lru_id')
        document_number = request.form.get('document_number')
        version = request.form.get('version')
        revision = request.form.get('revision')
        doc_ver = request.form.get('doc_ver')
        uploaded_by = request.form.get('uploaded_by')
        
        # Validate required fields
        if not all([lru_id, document_number, version, uploaded_by]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({"success": False, "message": "File type not allowed"}), 400
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        if file_size > MAX_FILE_SIZE:
            return jsonify({"success": False, "message": "File too large. Maximum size is 50MB"}), 400
        
        cur = conn.cursor()
        
        # Verify LRU exists
        cur.execute("SELECT lru_id FROM lrus WHERE lru_id = %s", (lru_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "LRU not found"}), 404
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save file to local storage
        file.save(file_path)
        
        # Insert plan document with actual file path
        cur.execute("""
            INSERT INTO plan_documents 
            (lru_id, document_number, version, revision, doc_ver, uploaded_by, file_path, status, original_filename, file_size, upload_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'not assigned', %s, %s, %s)
            RETURNING document_id
        """, (lru_id, document_number, version, revision, doc_ver, uploaded_by, file_path, file.filename, file_size, datetime.now()))
        
        document_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Plan document uploaded successfully",
            "document_id": document_id,
            "file_path": file_path,
            "original_filename": file.filename
        })
        
    except Exception as e:
        conn.rollback()
        # Clean up file if database insert failed
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        print(f"Error uploading plan document: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Update plan document status
@app.route('/api/plan-documents/<int:document_id>/status', methods=['PUT'])
def update_plan_document_status(document_id):
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        new_status = data.get('status')
        if not new_status:
            return jsonify({"success": False, "message": "Status is required"}), 400
        
        # Validate status
        valid_statuses = ['cleared', 'disapproved', 'assigned and returned', 'moved to next stage', 'not cleared', 'not assigned']
        if new_status not in valid_statuses:
            return jsonify({"success": False, "message": "Invalid status"}), 400
        
        cur = conn.cursor()
        
        # Update document status
        cur.execute("""
            UPDATE plan_documents 
            SET status = %s
            WHERE document_id = %s AND is_active = TRUE
            RETURNING document_id
        """, (new_status, document_id))
        
        result = cur.fetchone()
        if not result:
            cur.close()
            return jsonify({"success": False, "message": "Document not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Document status updated successfully"
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating plan document status: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Serve uploaded files
@app.route('/api/files/plan-documents/<path:filename>', methods=['GET'])
def serve_plan_document(filename):
    """Serve uploaded plan document files"""
    try:
        print(f"📁 Request to serve file: {filename}")
        print(f"📂 Upload folder: {UPLOAD_FOLDER}")
        
        # Clean the filename - remove any path separators
        clean_filename = os.path.basename(filename)
        file_path = os.path.join(UPLOAD_FOLDER, clean_filename)
        
        print(f"🔍 Looking for file at: {file_path}")
        print(f"📄 File exists: {os.path.exists(file_path)}")
        
        if os.path.exists(file_path):
            print(f"📊 File size: {os.path.getsize(file_path)} bytes")
        
        # List files in upload directory for debugging
        try:
            files_in_dir = os.listdir(UPLOAD_FOLDER)
            print(f"📋 Files in upload directory: {files_in_dir}")
        except Exception as list_error:
            print(f"❌ Error listing directory: {list_error}")
        
        # Security check - ensure file is within upload directory
        abs_upload_folder = os.path.abspath(UPLOAD_FOLDER)
        abs_file_path = os.path.abspath(file_path)
        
        if not abs_file_path.startswith(abs_upload_folder):
            print(f"🚫 Security violation: File path outside upload directory")
            return jsonify({"success": False, "message": "Invalid file path"}), 403
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return jsonify({"success": False, "message": f"File not found: {clean_filename}"}), 404
        
        print(f"✅ Serving file: {file_path}")
        return send_file(file_path, as_attachment=False)
        
    except Exception as e:
        print(f"❌ Error serving file {filename}: {str(e)}")
        return jsonify({"success": False, "message": f"Error serving file: {str(e)}"}), 500

# Get document details for display
@app.route('/api/plan-documents/<int:document_id>', methods=['GET'])
def get_plan_document(document_id):
    """Get plan document details including file path"""
    try:
        cur = conn.cursor()
        
        cur.execute("""
            SELECT pd.document_id, pd.lru_id, pd.document_number, pd.version, pd.revision, 
                   pd.doc_ver, pd.uploaded_by, pd.file_path, pd.status, pd.original_filename, 
                   pd.file_size, pd.upload_date, u.name as uploaded_by_name, l.lru_name
            FROM plan_documents pd
            LEFT JOIN users u ON pd.uploaded_by = u.user_id
            LEFT JOIN lrus l ON pd.lru_id = l.lru_id
            WHERE pd.document_id = %s
        """, (document_id,))
        
        document = cur.fetchone()
        cur.close()
        
        if not document:
            return jsonify({"success": False, "message": "Document not found"}), 404
        
        return jsonify({
            "success": True,
            "document": {
                "document_id": document[0],
                "lru_id": document[1],
                "document_number": document[2],
                "version": document[3],
                "revision": document[4],
                "doc_ver": document[5],
                "uploaded_by": document[6],
                "file_path": document[7],
                "status": document[8],
                "original_filename": document[9],
                "file_size": document[10],
                "upload_date": document[11].isoformat() if document[11] else None,
                "uploaded_by_name": document[12],
                "lru_name": document[13]
            }
        })
        
    except Exception as e:
        print(f"Error fetching document {document_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Get next doc_ver for an LRU
@app.route('/api/plan-documents/next-doc-ver/<int:lru_id>', methods=['GET'])
def get_next_doc_ver(lru_id):
    """Get the next doc_ver number for a specific LRU"""
    try:
        cur = conn.cursor()
        
        # Get the highest doc_ver for this LRU
        cur.execute("""
            SELECT MAX(CAST(doc_ver AS INTEGER)) 
            FROM plan_documents 
            WHERE lru_id = %s
        """, (lru_id,))
        
        result = cur.fetchone()
        cur.close()
        
        # If no documents exist for this LRU, start with 1
        max_doc_ver = result[0] if result[0] is not None else 0
        next_doc_ver = max_doc_ver + 1
        
        return jsonify({
            "success": True,
            "nextDocVer": next_doc_ver,
            "lruId": lru_id
        })
        
    except Exception as e:
        print(f"Error getting next doc_ver for LRU {lru_id}: {str(e)}")
        # Rollback the transaction to clear the error state
        try:
            conn.rollback()
        except:
            pass
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Get LRU and project metadata
@app.route('/api/lrus/<int:lru_id>/metadata', methods=['GET'])
def get_lru_metadata(lru_id):
    """Get LRU and associated project metadata"""
    try:
        cur = conn.cursor()
        
        cur.execute("""
            SELECT l.lru_id, l.lru_name, l.project_id,
                   p.project_name
            FROM lrus l
            LEFT JOIN projects p ON l.project_id = p.project_id
            WHERE l.lru_id = %s
        """, (lru_id,))
        
        result = cur.fetchone()
        cur.close()
        
        if not result:
            return jsonify({"success": False, "message": "LRU not found"}), 404
        
        return jsonify({
            "success": True,
            "lru": {
                "lru_id": result[0],
                "lru_name": result[1],
                "project_id": result[2],
                "project_name": result[3]
            }
        })
        
    except Exception as e:
        print(f"Error getting LRU metadata for {lru_id}: {str(e)}")
        # Rollback the transaction to clear the error state
        try:
            conn.rollback()
        except:
            pass
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Tests and Stages endpoints

# Get all tests
@app.route('/api/tests', methods=['GET'])
def get_tests():
    try:
        cur = conn.cursor()
        
        cur.execute("""
            SELECT test_id, test_name, created_at
            FROM tests
            ORDER BY test_id
        """)
        
        tests = cur.fetchall()
        cur.close()
        
        test_list = []
        for test in tests:
            test_list.append({
                "test_id": test[0],
                "test_name": test[1],
                "created_at": test[2].isoformat() if test[2] else None
            })
        
        return jsonify({
            "success": True,
            "tests": test_list
        })
        
    except Exception as e:
        print(f"Error fetching tests: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Get all stages
@app.route('/api/stages', methods=['GET'])
def get_stages():
    try:
        cur = conn.cursor()
        
        cur.execute("""
            SELECT stage_id, stage_name, created_at
            FROM stages
            ORDER BY stage_id
        """)
        
        stages = cur.fetchall()
        cur.close()
        
        stage_list = []
        for stage in stages:
            stage_list.append({
                "stage_id": stage[0],
                "stage_name": stage[1],
                "created_at": stage[2].isoformat() if stage[2] else None
            })
        
        return jsonify({
            "success": True,
            "stages": stage_list
        })
        
    except Exception as e:
        print(f"Error fetching stages: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Get all stage types
@app.route('/api/stage-types', methods=['GET'])
def get_stage_types():
    try:
        cur = conn.cursor()
        
        cur.execute("""
            SELECT type_id, type_name
            FROM stage_types
            ORDER BY type_name
        """)
        
        types = cur.fetchall()
        cur.close()
        
        type_list = []
        for stage_type in types:
            type_list.append({
                "type_id": stage_type[0],
                "type_name": stage_type[1]
            })
        
        return jsonify({
            "success": True,
            "stage_types": type_list
        })
        
    except Exception as e:
        print(f"Error fetching stage types: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Get complete test configuration matrix
@app.route('/api/tests-configuration', methods=['GET'])
def get_tests_configuration():
    try:
        cur = conn.cursor()
        
        # Get all tests
        cur.execute("""
            SELECT test_id, test_name, created_at
            FROM tests
            ORDER BY test_id
        """)
        tests = cur.fetchall()
        
        # Get all stages
        cur.execute("""
            SELECT stage_id, stage_name, created_at
            FROM stages
            ORDER BY stage_id
        """)
        stages = cur.fetchall()
        
        # Get all stage types
        cur.execute("""
            SELECT type_id, type_name
            FROM stage_types
            ORDER BY type_name
        """)
        stage_types = cur.fetchall()
        
        # Get current configurations
        cur.execute("""
            SELECT 
                tst.test_id,
                tst.stage_id,
                tst.type_id,
                t.test_name,
                s.stage_name,
                st.type_name
            FROM test_stage_types tst
            JOIN tests t ON tst.test_id = t.test_id
            JOIN stages s ON tst.stage_id = s.stage_id
            JOIN stage_types st ON tst.type_id = st.type_id
            ORDER BY t.test_id, s.stage_id
        """)
        configurations = cur.fetchall()
        
        cur.close()
        
        # Format tests
        test_list = []
        for test in tests:
            test_list.append({
                "test_id": test[0],
                "test_name": test[1],
                "created_at": test[2].isoformat() if test[2] else None
            })
        
        # Format stages
        stage_list = []
        for stage in stages:
            stage_list.append({
                "stage_id": stage[0],
                "stage_name": stage[1],
                "created_at": stage[2].isoformat() if stage[2] else None
            })
        
        # Format stage types
        type_list = []
        for stage_type in stage_types:
            type_list.append({
                "type_id": stage_type[0],
                "type_name": stage_type[1]
            })
        
        # Format configurations
        config_list = []
        for config in configurations:
            config_list.append({
                "test_id": config[0],
                "stage_id": config[1],
                "type_id": config[2],
                "test_name": config[3],
                "stage_name": config[4],
                "type_name": config[5]
            })
        
        return jsonify({
            "success": True,
            "tests": test_list,
            "stages": stage_list,
            "stage_types": type_list,
            "configurations": config_list
        })
        
    except Exception as e:
        print(f"Error fetching test configuration matrix: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Get test-stage-type configurations (legacy endpoint)
@app.route('/api/test-stage-types', methods=['GET'])
def get_test_stage_types():
    try:
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                tst.test_id,
                tst.stage_id,
                tst.type_id,
                t.test_name,
                s.stage_name,
                st.type_name
            FROM test_stage_types tst
            JOIN tests t ON tst.test_id = t.test_id
            JOIN stages s ON tst.stage_id = s.stage_id
            JOIN stage_types st ON tst.type_id = st.type_id
            ORDER BY t.test_id, s.stage_id
        """)
        
        configurations = cur.fetchall()
        cur.close()
        
        config_list = []
        for config in configurations:
            config_list.append({
                "test_id": config[0],
                "stage_id": config[1],
                "type_id": config[2],
                "test_name": config[3],
                "stage_name": config[4],
                "type_name": config[5]
            })
        
        return jsonify({
            "success": True,
            "configurations": config_list
        })
        
    except Exception as e:
        print(f"Error fetching test-stage-type configurations: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Create new test
@app.route('/api/tests', methods=['POST'])
def create_test():
    try:
        data = request.json
        if not data or not data.get('test_name'):
            return jsonify({"success": False, "message": "Test name is required"}), 400
        
        cur = conn.cursor()
        
        # Check if test name already exists
        cur.execute("SELECT test_id FROM tests WHERE test_name = %s", (data['test_name'],))
        if cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Test name already exists"}), 400
        
        # Insert new test
        cur.execute("""
            INSERT INTO tests (test_name)
            VALUES (%s)
            RETURNING test_id
        """, (data['test_name'],))
        
        test_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Test created successfully",
            "test_id": test_id
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error creating test: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Create new stage
@app.route('/api/stages', methods=['POST'])
def create_stage():
    try:
        data = request.json
        if not data or not data.get('stage_name'):
            return jsonify({"success": False, "message": "Stage name is required"}), 400
        
        cur = conn.cursor()
        
        # Check if stage name already exists
        cur.execute("SELECT stage_id FROM stages WHERE stage_name = %s", (data['stage_name'],))
        if cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Stage name already exists"}), 400
        
        # Insert new stage
        cur.execute("""
            INSERT INTO stages (stage_name)
            VALUES (%s)
            RETURNING stage_id
        """, (data['stage_name'],))
        
        stage_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Stage created successfully",
            "stage_id": stage_id
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error creating stage: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Update test-stage-type configurations
@app.route('/api/test-stage-types', methods=['POST'])
def update_test_stage_types():
    try:
        data = request.json
        if not data or 'configurations' not in data:
            return jsonify({"success": False, "message": "Configurations data is required"}), 400
        
        # Get current user from request (you might want to implement proper auth)
        current_user = data.get('assigned_by', 1002)  # Default user for now
        
        cur = conn.cursor()
        
        # Clear existing configurations
        cur.execute("DELETE FROM test_stage_types")
        
        # Insert new configurations
        for config in data['configurations']:
            if config.get('test_id') and config.get('stage_id') and config.get('type_id'):
                cur.execute("""
                    INSERT INTO test_stage_types (test_id, stage_id, type_id, assigned_by)
                    VALUES (%s, %s, %s, %s)
                """, (config['test_id'], config['stage_id'], config['type_id'], current_user))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Test-stage-type configurations updated successfully"
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating test-stage-type configurations: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Delete test
@app.route('/api/tests/<int:test_id>', methods=['DELETE'])
def delete_test(test_id):
    try:
        cur = conn.cursor()
        
        # Delete test-stage-type configurations first
        cur.execute("DELETE FROM test_stage_types WHERE test_id = %s", (test_id,))
        
        # Delete test
        cur.execute("DELETE FROM tests WHERE test_id = %s RETURNING test_id", (test_id,))
        deleted = cur.fetchone()
        
        if not deleted:
            cur.close()
            return jsonify({"success": False, "message": "Test not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Test deleted successfully"
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error deleting test: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Delete stage
@app.route('/api/stages/<int:stage_id>', methods=['DELETE'])
def delete_stage(stage_id):
    try:
        cur = conn.cursor()
        
        # Delete test-stage-type configurations for this stage first
        cur.execute("DELETE FROM test_stage_types WHERE stage_id = %s", (stage_id,))
        
        # Delete stage
        cur.execute("DELETE FROM stages WHERE stage_id = %s RETURNING stage_id", (stage_id,))
        deleted = cur.fetchone()
        
        if not deleted:
            cur.close()
            return jsonify({"success": False, "message": "Stage not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Stage deleted successfully"
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error deleting stage: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Diagnostic endpoint to check database contents
@app.route('/api/tests-debug', methods=['GET'])
def get_tests_debug():
    try:
        cur = conn.cursor()
        
        # Check tests table
        cur.execute("SELECT COUNT(*) FROM tests")
        test_count = cur.fetchone()[0]
        
        cur.execute("SELECT test_id, test_name FROM tests LIMIT 5")
        test_samples = cur.fetchall()
        
        # Check stages table
        cur.execute("SELECT COUNT(*) FROM stages")
        stage_count = cur.fetchone()[0]
        
        cur.execute("SELECT stage_id, stage_name FROM stages LIMIT 5")
        stage_samples = cur.fetchall()
        
        # Check stage_types table
        cur.execute("SELECT COUNT(*) FROM stage_types")
        type_count = cur.fetchone()[0]
        
        cur.execute("SELECT type_id, type_name FROM stage_types LIMIT 5")
        type_samples = cur.fetchall()
        
        # Check test_stage_types table
        cur.execute("SELECT COUNT(*) FROM test_stage_types")
        config_count = cur.fetchone()[0]
        
        cur.execute("""
            SELECT tst.test_id, tst.stage_id, tst.type_id, t.test_name, s.stage_name, st.type_name
            FROM test_stage_types tst
            JOIN tests t ON tst.test_id = t.test_id
            JOIN stages s ON tst.stage_id = s.stage_id
            JOIN stage_types st ON tst.type_id = st.type_id
            LIMIT 5
        """)
        config_samples = cur.fetchall()
        
        cur.close()
        
        return jsonify({
            "success": True,
            "debug_info": {
                "tests": {
                    "count": test_count,
                    "samples": [{"test_id": t[0], "test_name": t[1]} for t in test_samples]
                },
                "stages": {
                    "count": stage_count,
                    "samples": [{"stage_id": s[0], "stage_name": s[1]} for s in stage_samples]
                },
                "stage_types": {
                    "count": type_count,
                    "samples": [{"type_id": st[0], "type_name": st[1]} for st in type_samples]
                },
                "configurations": {
                    "count": config_count,
                    "samples": [{"test_id": c[0], "stage_id": c[1], "type_id": c[2], "test_name": c[3], "stage_name": c[4], "type_name": c[5]} for c in config_samples]
                }
            }
        })
        
    except Exception as e:
        print(f"Debug error: {str(e)}")
        return jsonify({"success": False, "message": f"Debug error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
