"""
User management routes
"""
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import hash_password, handle_database_error

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/roles', methods=['GET'])
def get_roles():
    """Get all roles"""
    try:
        conn = get_db_connection()
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

@users_bp.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
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
        
        conn = get_db_connection()
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
        return handle_database_error(get_db_connection(), f"Error creating user: {str(e)}")

@users_bp.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        conn = get_db_connection()
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
        return handle_database_error(get_db_connection(), f"Error updating user: {str(e)}")

@users_bp.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get single user with role information"""
    try:
        conn = get_db_connection()
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

@users_bp.route('/api/users/manage', methods=['GET'])
def get_users_with_roles():
    """Get users with roles for management"""
    try:
        conn = get_db_connection()
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

@users_bp.route('/api/available-reviewers', methods=['GET'])
def get_available_reviewers():
    """Get list of users who can be assigned as reviewers"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch users with QA Reviewer role (role_id = 3)
        cur.execute("""
            SELECT u.user_id, u.name, u.email, r.role_name
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            WHERE ur.role_id = 3
            ORDER BY u.name
        """)
        
        reviewers = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        reviewer_list = []
        for reviewer in reviewers:
            reviewer_list.append({
                "id": reviewer[0],
                "name": reviewer[1],
                "email": reviewer[2],
                "role": reviewer[3],
                "available": True  # For now, assume all are available
            })
        
        return jsonify({
            "success": True,
            "reviewers": reviewer_list
        })
        
    except Exception as e:
        print(f"Error fetching available reviewers: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@users_bp.route('/api/test-qa-reviewers', methods=['GET'])
def test_qa_reviewers():
    """Test endpoint to verify QA Reviewer data"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Show all roles
        cur.execute("SELECT role_id, role_name FROM roles ORDER BY role_id")
        roles = cur.fetchall()
        
        # Show all user-role assignments
        cur.execute("""
            SELECT u.user_id, u.name, ur.role_id, r.role_name
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            ORDER BY u.user_id
        """)
        user_roles = cur.fetchall()
        
        # Show only QA Reviewers (role_id = 3)
        cur.execute("""
            SELECT u.user_id, u.name, u.email, r.role_name
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            WHERE ur.role_id = 3
            ORDER BY u.name
        """)
        qa_reviewers = cur.fetchall()
        
        cur.close()
        
        return jsonify({
            "success": True,
            "roles": [{"role_id": r[0], "role_name": r[1]} for r in roles],
            "user_roles": [{"user_id": ur[0], "name": ur[1], "role_id": ur[2], "role_name": ur[3]} for ur in user_roles],
            "qa_reviewers": [{"user_id": qr[0], "name": qr[1], "email": qr[2], "role_name": qr[3]} for qr in qa_reviewers]
        })
        
    except Exception as e:
        print(f"Test QA Reviewers error: {str(e)}")
        return jsonify({"success": False, "message": f"Test error: {str(e)}"}), 500
