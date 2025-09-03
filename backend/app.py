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
    password="Admin",
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
            SELECT u.user_id, u.name, u.email, u.password_hash, r.role_id, r.role_name
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
    try:
        cur = conn.cursor()
        
        # Fetch all projects from the projects table
        cur.execute("""
            SELECT project_id, project_name, description, created_at
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
                "description": project[2],
                "created_at": project[3].isoformat() if project[3] else None
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

if __name__ == '__main__':
    app.run(debug=True)
