"""
Activity logging utilities for tracking user actions
"""
from datetime import datetime
from config import get_db_connection
from utils.helpers import handle_database_error

def log_activity(project_id: int = None, activity_performed: str = None, performed_by: int = None, additional_info: str = None, user_id: int = None):
    """
    Log an activity to the activity_logs table
    
    Args:
        project_id (int, optional): ID of the project related to the activity
        activity_performed (str): Description of the activity performed
        performed_by (int): User ID who performed the activity
        additional_info (str, optional): Additional information about the activity
        user_id (int, optional): ID of the user related to the activity (for user operations)
    
    Returns:
        bool: True if logging was successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert activity log
        cur.execute("""
            INSERT INTO activity_logs (project_id, activity_performed, performed_by, additional_info)
            VALUES (%s, %s, %s, %s)
        """, (project_id, activity_performed, performed_by, additional_info))
        
        conn.commit()
        cur.close()
        return True
        
    except Exception as e:
        print(f"Error logging activity: {str(e)}")
        # Don't raise the error to avoid breaking the main operation
        return False

def get_activity_logs(project_id: int = None, limit: int = 100):
    """
    Retrieve activity logs
    
    Args:
        project_id (int, optional): Filter by specific project ID
        limit (int): Maximum number of logs to return
    
    Returns:
        list: List of activity log dictionaries
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if project_id:
            cur.execute("""
                SELECT al.activity_id, al.project_id, al.activity_performed, 
                       al.performed_by, al.timestamp, al.additional_info,
                       u.name as user_name, p.project_name
                FROM activity_logs al
                LEFT JOIN users u ON al.performed_by = u.user_id
                LEFT JOIN projects p ON al.project_id = p.project_id
                WHERE al.project_id = %s
                ORDER BY al.timestamp ASC
                LIMIT %s
            """, (project_id, limit))
        else:
            cur.execute("""
                SELECT al.activity_id, al.project_id, al.activity_performed, 
                       al.performed_by, al.timestamp, al.additional_info,
                       u.name as user_name, p.project_name
                FROM activity_logs al
                LEFT JOIN users u ON al.performed_by = u.user_id
                LEFT JOIN projects p ON al.project_id = p.project_id
                ORDER BY al.timestamp ASC
                LIMIT %s
            """, (limit,))
        
        logs = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        log_list = []
        for log in logs:
            log_list.append({
                "activity_id": log[0],
                "project_id": log[1],
                "activity_performed": log[2],
                "performed_by": log[3],
                "timestamp": log[4].isoformat() if log[4] else None,
                "additional_info": log[5],
                "user_name": log[6],
                "project_name": log[7]
            })
        
        return log_list
        
    except Exception as e:
        print(f"Error fetching activity logs: {str(e)}")
        return []
