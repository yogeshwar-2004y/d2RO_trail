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
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create tech_support_requests table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tech_support_requests (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                user_id VARCHAR(255) NOT NULL,
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
            data['userId'],
            data['date'],
            data['issue']
        ))
        
        conn.commit()
        cur.close()
        
        # Log the activity
        log_activity(
            user_id=data['username'],
            action="TECH_SUPPORT_REQUEST",
            details=f"Tech support request submitted by {data['username']} (User ID: {data['userId']})"
        )
        
        return jsonify({
            "success": True,
            "message": "Tech support request submitted successfully"
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error submitting tech support request: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tech_support_bp.route('/api/tech-support', methods=['GET'])
def get_tech_support_requests():
    """Get all tech support requests (admin only)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, username, user_id, issue_date, issue_description, 
                   status, created_at, updated_at
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
                "updated_at": req[7].isoformat() if req[7] else None
            })
        
        return jsonify({
            "success": True,
            "requests": request_list
        })
        
    except Exception as e:
        print(f"Error fetching tech support requests: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tech_support_bp.route('/api/tech-support/<int:request_id>/status', methods=['PUT'])
def update_tech_support_status():
    """Update tech support request status (admin only)"""
    try:
        data = request.json
        if not data or 'status' not in data:
            return jsonify({"success": False, "message": "Status is required"}), 400
        
        valid_statuses = ['pending', 'in_progress', 'resolved', 'closed']
        if data['status'] not in valid_statuses:
            return jsonify({"success": False, "message": "Invalid status"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE tech_support_requests 
            SET status = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (data['status'], request_id))
        
        if cur.rowcount == 0:
            return jsonify({"success": False, "message": "Request not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Status updated successfully"
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error updating tech support status: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500
