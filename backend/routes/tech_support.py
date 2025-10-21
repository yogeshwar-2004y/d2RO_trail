"""
Tech support management routes
"""
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import handle_database_error
from utils.activity_logger import log_activity
from datetime import datetime

tech_support_bp = Blueprint('tech_support', __name__)

@tech_support_bp.route('/api/tech-support', methods=['POST'])
def submit_tech_support():
    """Submit a tech support request"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['username', 'userId', 'date', 'issue']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        # Validate user_id is a valid integer
        try:
            user_id = int(data['userId'])
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "User ID must be a valid number"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create tech_support_requests table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tech_support_requests (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                user_id INTEGER NOT NULL,
                issue_date DATE NOT NULL,
                issue_description TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert the tech support request
        cur.execute("""
            INSERT INTO tech_support_requests (username, user_id, issue_date, issue_description)
            VALUES (%s, %s, %s, %s)
        """, (
            data['username'],
            user_id,  # Use validated user_id
            data['date'],
            data['issue']
        ))
        
        conn.commit()
        cur.close()
        
        # Log the activity
        try:
            log_activity(
                user_id=data['username'],
                action="TECH_SUPPORT_REQUEST",
                details=f"Tech support request submitted by {data['username']} (User ID: {data['userId']})"
            )
        except Exception as log_error:
            print(f"Warning: Failed to log activity: {str(log_error)}")
            # Continue execution even if logging fails
        
        return jsonify({
            "success": True,
            "message": "Tech support request submitted successfully"
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error submitting tech support request: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

@tech_support_bp.route('/api/tech-support/user/<user_id>', methods=['GET'])
def get_user_tech_support_requests(user_id):
    """Get tech support requests for a specific user"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, username, user_id, issue_date, issue_description, 
                   status, created_at, updated_at, status_updated_by, status_updated_at
            FROM tech_support_requests
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))
        
        requests = cur.fetchall()
        cur.close()
        
        request_list = []
        for req in requests:
            request_list.append({
                "id": req[0],
                "username": req[1],
                "user_id": req[2],
                "issue_date": req[3].isoformat() if req[3] else None,
                "issue_description": req[4],
                "status": req[5],
                "created_at": req[6].isoformat() if req[6] else None,
                "updated_at": req[7].isoformat() if req[7] else None,
                "status_updated_by": req[8],
                "status_updated_at": req[9].isoformat() if req[9] else None
            })
        
        return jsonify({
            "success": True,
            "requests": request_list,
            "total_count": len(request_list)
        })
        
    except Exception as e:
        print(f"Error fetching user tech support requests: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tech_support_bp.route('/api/tech-support', methods=['GET'])
def get_tech_support_requests():
    """Get all tech support requests (admin only)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, username, user_id, issue_date, issue_description, 
                   status, created_at, updated_at, status_updated_by, status_updated_at
            FROM tech_support_requests
            ORDER BY created_at DESC
        """)
        
        requests = cur.fetchall()
        cur.close()
        
        request_list = []
        for req in requests:
            request_list.append({
                "id": req[0],
                "username": req[1],
                "user_id": req[2],
                "issue_date": req[3].isoformat() if req[3] else None,
                "issue_description": req[4],
                "status": req[5],
                "created_at": req[6].isoformat() if req[6] else None,
                "updated_at": req[7].isoformat() if req[7] else None,
                "status_updated_by": req[8],
                "status_updated_at": req[9].isoformat() if req[9] else None
            })
        
        return jsonify({
            "success": True,
            "requests": request_list
        })
        
    except Exception as e:
        print(f"Error fetching tech support requests: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tech_support_bp.route('/api/tech-support/<int:request_id>/status', methods=['PUT'])
def update_tech_support_status(request_id):
    """Update tech support request status (admin only)"""
    try:
        data = request.json
        if not data or 'status' not in data:
            return jsonify({"success": False, "message": "Status is required"}), 400
        
        # Get admin user info from request headers or body
        admin_user_id = data.get('admin_user_id')
        if not admin_user_id:
            return jsonify({"success": False, "message": "Admin user ID is required"}), 400
        
        valid_statuses = ['pending', 'in_progress', 'resolved', 'closed']
        if data['status'] not in valid_statuses:
            return jsonify({"success": False, "message": "Invalid status"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Update the status with tracking information
        cur.execute("""
            UPDATE tech_support_requests 
            SET status = %s, 
                status_updated_by = %s,
                status_updated_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (data['status'], admin_user_id, request_id))
        
        if cur.rowcount == 0:
            return jsonify({"success": False, "message": "Request not found"}), 404
        
        conn.commit()
        cur.close()
        
        # Log the activity
        try:
            log_activity(
                user_id=str(admin_user_id),
                action="TECH_SUPPORT_STATUS_UPDATE",
                details=f"Updated tech support request #{request_id} status to {data['status']}"
            )
        except Exception as log_error:
            print(f"Warning: Failed to log activity: {str(log_error)}")
        
        return jsonify({
            "success": True,
            "message": "Status updated successfully"
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error updating tech support status: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500