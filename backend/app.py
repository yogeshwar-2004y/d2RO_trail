from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import hashlib
import os

app = Flask(__name__)
CORS(app)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return hash_password(password) == hashed_password
    #return password == hashed_password

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="ERP",
    user="postgres",
    password="thani123",
    host="localhost",
    port="5432"
)

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
            SELECT u.user_id, u.name, u.email, u.password_hash, r.role_name
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            WHERE u.email = %s
        """, (email,))
        
        user = cur.fetchone()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 401

        # Check if password matches (assuming password_hash stores the actual password for now)
        if verify_password(password, user[3]):
            cur.close()
            return jsonify({
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "role": user[4]  # role_name from roles table
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
                "uploaded_by_name": doc[9],
                "upload_date": doc[6].isoformat() if doc[6] else None,
                "file_path": doc[7],
                "status": doc[8]
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
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        lru_id = data.get('lru_id')
        document_number = data.get('document_number')
        version = data.get('version')
        revision = data.get('revision')
        doc_ver = data.get('doc_ver')
        uploaded_by = data.get('uploaded_by')
        file_path = data.get('file_path')
        
        if not all([lru_id, document_number, version, uploaded_by, file_path]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        cur = conn.cursor()
        
        # Verify LRU exists
        cur.execute("SELECT lru_id FROM lrus WHERE lru_id = %s", (lru_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "LRU not found"}), 404
        
        # Insert plan document
        cur.execute("""
            INSERT INTO plan_documents 
            (lru_id, document_number, version, revision, doc_ver, uploaded_by, file_path, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'not assigned')
            RETURNING document_id
        """, (lru_id, document_number, version, revision, doc_ver, uploaded_by, file_path))
        
        document_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Plan document uploaded successfully",
            "document_id": document_id
        })
        
    except Exception as e:
        conn.rollback()
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

if __name__ == '__main__':
    app.run(debug=True)
