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

def get_activity_logs(project_id: int = None, limit: int = 100, search: str = None,
                     user_name: str = None, activity_id: str = None, 
                     project_id_filter: str = None, activity_type: str = None,
                     date_from: str = None, date_to: str = None):
    """
    Retrieve activity logs
    
    Args:
        project_id (int, optional): Filter by specific project ID
        limit (int): Maximum number of logs to return
        search (str, optional): General search query to filter logs
        user_name (str, optional): Filter by user name
        activity_id (str, optional): Filter by activity ID
        project_id_filter (str, optional): Filter by project ID (as string for partial match)
        activity_type (str, optional): Filter by activity type
        date_from (str, optional): Filter by date from (YYYY-MM-DD)
        date_to (str, optional): Filter by date to (YYYY-MM-DD)
    
    Returns:
        list: List of activity log dictionaries
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if notification columns exist
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'activity_logs' AND column_name = 'notification_type'
        """)
        has_notification_columns = cur.fetchone() is not None
        
        # Build base query
        if has_notification_columns:
            base_query = """
                SELECT al.activity_id, al.project_id, al.activity_performed, 
                       al.performed_by, al.timestamp, al.additional_info,
                       u.name as user_name, p.project_name
                FROM activity_logs al
                LEFT JOIN users u ON al.performed_by = u.user_id
                LEFT JOIN projects p ON al.project_id = p.project_id
                WHERE (al.notification_type IS NULL AND al.notified_user_id IS NULL)
            """
        else:
            base_query = """
                SELECT al.activity_id, al.project_id, al.activity_performed, 
                       al.performed_by, al.timestamp, al.additional_info,
                       u.name as user_name, p.project_name
                FROM activity_logs al
                LEFT JOIN users u ON al.performed_by = u.user_id
                LEFT JOIN projects p ON al.project_id = p.project_id
            """
        
        query_params = []
        where_conditions = []
        
        # Add project_id filter if provided (exact match)
        if project_id:
            where_conditions.append("al.project_id = %s")
            query_params.append(project_id)
        
        # Add general search filter if provided
        if search and search.strip():
            search_pattern = f'%{search.strip()}%'
            where_conditions.append("""(
                CAST(al.activity_id AS TEXT) ILIKE %s OR
                CAST(al.project_id AS TEXT) ILIKE %s OR
                LOWER(COALESCE(al.activity_performed, '')) ILIKE %s OR
                LOWER(COALESCE(u.name, '')) ILIKE %s OR
                LOWER(COALESCE(p.project_name, '')) ILIKE %s OR
                LOWER(COALESCE(al.additional_info, '')) ILIKE %s
            )""")
            query_params.extend([search_pattern] * 6)
        
        # Add advanced filters
        if user_name and user_name.strip():
            where_conditions.append("COALESCE(u.name, '') ILIKE %s")
            query_params.append(f'%{user_name.strip()}%')
        
        if activity_id and activity_id.strip():
            where_conditions.append("CAST(al.activity_id AS TEXT) ILIKE %s")
            query_params.append(f'%{activity_id.strip()}%')
        
        if project_id_filter and project_id_filter.strip():
            where_conditions.append("CAST(al.project_id AS TEXT) ILIKE %s")
            query_params.append(f'%{project_id_filter.strip()}%')
        
        if activity_type and activity_type.strip():
            where_conditions.append("LOWER(COALESCE(al.activity_performed, '')) ILIKE %s")
            query_params.append(f'%{activity_type.strip().lower()}%')
        
        if date_from and date_from.strip():
            where_conditions.append("DATE(al.timestamp) >= %s")
            query_params.append(date_from.strip())
        
        if date_to and date_to.strip():
            where_conditions.append("DATE(al.timestamp) <= %s")
            query_params.append(date_to.strip())
        
        # Add WHERE conditions if any
        if where_conditions:
            base_query += " AND " + " AND ".join(where_conditions)
        
        # Add ORDER BY
        base_query += " ORDER BY al.timestamp DESC"
        
        # Only apply limit if no filters are active (to export all filtered results when filters are applied)
        # Check if any filter is provided (not None and not empty)
        has_any_filters = (
            (search and search.strip()) or
            (user_name and user_name.strip()) or
            (activity_id and activity_id.strip()) or
            (project_id_filter and project_id_filter.strip()) or
            (activity_type and activity_type.strip()) or
            (date_from and date_from.strip()) or
            (date_to and date_to.strip())
        )
        if not has_any_filters:
            base_query += " LIMIT %s"
            query_params.append(limit)
        
        # Debug: print query for troubleshooting
        print(f"Activity Logs Query: {base_query}")
        print(f"Activity Logs Params: {query_params}")
        
        # Execute query - handle empty params tuple
        if query_params:
            cur.execute(base_query, tuple(query_params))
        else:
            cur.execute(base_query)
        
        logs = cur.fetchall()
        print(f"Activity Logs found {len(logs)} logs")
        
        cur.close()
        
        # Convert to list of dictionaries
        log_list = []
        for log in logs:
            log_dict = {
                "activity_id": log[0],
                "project_id": log[1] if log[1] is not None else None,
                "activity_performed": log[2] if log[2] else None,
                "performed_by": log[3] if log[3] else None,
                "timestamp": log[4].isoformat() if log[4] else None,
                "additional_info": log[5] if log[5] else None,
                "user_name": log[6] if log[6] else None,
                "project_name": log[7] if log[7] else None
            }
            log_list.append(log_dict)
        
        print(f"Activity Logs returning {len(log_list)} logs")
        return log_list
        
    except Exception as e:
        print(f"Error fetching activity logs: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
