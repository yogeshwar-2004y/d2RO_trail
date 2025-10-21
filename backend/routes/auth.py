"""
Authentication routes for the Flask application
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from config import get_db_connection
from utils.helpers import verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api', methods=['GET'])
def hello_world():
    """Test endpoint"""
    return jsonify(message="Hello from Flask!")

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        conn = get_db_connection()
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
            # Log failed login attempt for non-existent user
            try:
                # For non-existent emails, we'll create a special entry with user_id = 0
                cur.execute("""
                    INSERT INTO login_logs (user_id, activity_performed, performed_by)
                    VALUES (%s, %s, %s)
                """, (0, 'LOGIN', 0))
                conn.commit()
            except Exception as log_error:
                print(f"Error logging failed login attempt for non-existent user: {str(log_error)}")
            
            cur.close()
            return jsonify({"success": False, "message": "User not found"}), 401

        # Check if password matches
        if verify_password(password, user[3]):
            # Log successful login
            try:
                cur.execute("""
                    INSERT INTO login_logs (user_id, activity_performed, performed_by)
                    VALUES (%s, %s, %s)
                """, (user[0], 'LOGIN', user[0]))
                conn.commit()
            except Exception as log_error:
                print(f"Error logging login activity: {str(log_error)}")
                # Don't fail login if logging fails
            
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
            # Log failed login attempt
            try:
                cur.execute("""
                    INSERT INTO login_logs (user_id, activity_performed, performed_by)
                    VALUES (%s, %s, %s)
                """, (user[0], 'LOGIN', user[0]))
                conn.commit()
            except Exception as log_error:
                print(f"Error logging failed login attempt: {str(log_error)}")
            
            cur.close()
            print(f"Invalid password for user {email} with password as {password}")
            return jsonify({"success": False, "message": "Invalid password"}), 401
            
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
            
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"success": False, "message": "user_id is required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Log logout activity
        try:
            cur.execute("""
                INSERT INTO login_logs (user_id, activity_performed, performed_by)
                VALUES (%s, %s, %s)
            """, (user_id, 'LOGOUT', user_id))
            conn.commit()
        except Exception as log_error:
            print(f"Error logging logout activity: {str(log_error)}")
            # Don't fail logout if logging fails
        
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Logout successful"
        })
        
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500
