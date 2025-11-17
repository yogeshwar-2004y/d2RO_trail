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

def log_notification(project_id: int = None, activity_performed: str = None, performed_by: int = None, notified_user_id: int = None, notification_type: str = None, additional_info: str = None):
    """
    Log a notification to the activity_logs table
    
    Args:
        project_id (int, optional): ID of the project related to the notification
        activity_performed (str): Description of the activity/notification
        performed_by (int): User ID who performed the activity
        notified_user_id (int): User ID who should receive the notification
        notification_type (str): Type of notification (e.g., 'project_created')
        additional_info (str, optional): Additional information about the notification
    
    Returns:
        bool: True if logging was successful, False otherwise
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert notification log
        cur.execute("""
            INSERT INTO activity_logs (project_id, activity_performed, performed_by, notified_user_id, notification_type, is_read, additional_info)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (project_id, activity_performed, performed_by, notified_user_id, notification_type, False, additional_info))
        
        conn.commit()
        print(f"DEBUG log_notification: Notification inserted for user_id={notified_user_id}, type={notification_type}, activity='{activity_performed}'")
        return True
        
    except Exception as e:
        print(f"Error logging notification: {str(e)}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
        return False
    finally:
        if cur:
            cur.close()
        # Don't close conn - it's a shared global connection

def get_users_by_role(role_id: int):
    """
    Get all users with a specific role
    
    Args:
        role_id (int): The role ID to filter by
    
    Returns:
        list: List of user dictionaries with user_id, name, and email
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT u.user_id, u.name, u.email
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            WHERE ur.role_id = %s
        """, (role_id,))
        
        users = cur.fetchall()
        
        user_list = []
        for user in users:
            user_list.append({
                "user_id": user[0],
                "name": user[1],
                "email": user[2]
            })
        
        print(f"DEBUG get_users_by_role: Found {len(user_list)} user(s) with role_id={role_id}")
        return user_list
        
    except Exception as e:
        print(f"Error fetching users by role: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if cur:
            cur.close()
        # Don't close conn - it's a shared global connection

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
                  AND (al.notification_type IS NULL AND al.notified_user_id IS NULL)
                ORDER BY al.timestamp DESC
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
                WHERE (al.notification_type IS NULL AND al.notified_user_id IS NULL)
                ORDER BY al.timestamp DESC
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
