"""
Authentication routes for the Flask application
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from config import get_db_connection
from utils.helpers import verify_password
from utils.suspicious_activity import (
    check_password_change_frequency, 
    is_late_night_login, 
    log_failed_login_attempt,
    log_suspicious_activity
)

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
                    INSERT INTO login_logs (user_id, activity_performed, performed_by, 
                                           is_suspicious, suspicion_reason, failed_attempts_count)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (0, 'login_failed', 0, True, f'Failed login attempt for non-existent email: {email}', 1))
                conn.commit()
            except Exception as log_error:
                print(f"Error logging failed login attempt for non-existent user: {str(log_error)}")
            
            cur.close()
            return jsonify({"success": False, "message": "User not found"}), 401

        # Check if password matches
        if verify_password(password, user[3]):
            # Check for suspicious activities
            suspicion_reasons = []
            is_suspicious = False
            
            # Check 1: Late night login (12 AM - 6 AM)
            current_time = datetime.now()
            if is_late_night_login(current_time):
                suspicion_reasons.append("Late night login (12 AM - 6 AM)")
                is_suspicious = True
            
            # Check 2: Password change frequency (more than 3 times in 24 hours)
            if check_password_change_frequency(user[0]):
                suspicion_reasons.append("Multiple password changes in 24 hours")
                is_suspicious = True
            
            # Log successful login with suspicious activity flags
            try:
                suspicion_reason = "; ".join(suspicion_reasons) if suspicion_reasons else None
                cur.execute("""
                    INSERT INTO login_logs (user_id, activity_performed, performed_by, 
                                           is_suspicious, suspicion_reason, failed_attempts_count)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user[0], 'logged_in', user[0], is_suspicious, suspicion_reason, 0))
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
                },
                "suspicious_activity": {
                    "is_suspicious": is_suspicious,
                    "reasons": suspicion_reasons
                }
            })
        else:
            # Log failed login attempt
            try:
                log_failed_login_attempt(user[0])
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
                INSERT INTO login_logs (user_id, activity_performed, performed_by, 
                                       is_suspicious, suspicion_reason, failed_attempts_count)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, 'logged_out', user_id, False, None, 0))
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
