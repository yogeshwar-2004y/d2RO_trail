"""
Suspicious Activity Detection Module
Detects and logs suspicious login activities
"""
from datetime import datetime, timedelta
from config import get_db_connection

def check_password_change_frequency(user_id, hours=24, max_changes=3):
    """
    Check if user has changed password more than max_changes times in the last hours
    Returns True if suspicious, False otherwise
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Calculate time threshold
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        # Count password change activities in the last 24 hours
        cur.execute("""
            SELECT COUNT(*) 
            FROM login_logs 
            WHERE user_id = %s 
            AND activity_performed = 'password_changed'
            AND timestamp >= %s
        """, (user_id, time_threshold))
        
        count = cur.fetchone()[0]
        cur.close()
        
        return count > max_changes
        
    except Exception as e:
        print(f"Error checking password change frequency: {e}")
        return False

def is_late_night_login(timestamp):
    """
    Check if login occurred between 12 AM and 6 AM
    Returns True if suspicious, False otherwise
    """
    try:
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        hour = timestamp.hour
        return hour >= 0 and hour < 6
        
    except Exception as e:
        print(f"Error checking late night login: {e}")
        return False

def check_failed_login_attempts(user_id, hours=24, max_attempts=7):
    """
    Check if user has failed login attempts more than max_attempts times in the last hours
    Returns count of failed attempts
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Calculate time threshold
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        # Count failed login attempts in the last 24 hours
        cur.execute("""
            SELECT COUNT(*) 
            FROM login_logs 
            WHERE user_id = %s 
            AND activity_performed = 'login_failed'
            AND timestamp >= %s
        """, (user_id, time_threshold))
        
        count = cur.fetchone()[0]
        cur.close()
        
        return count
        
    except Exception as e:
        print(f"Error checking failed login attempts: {e}")
        return 0

def log_suspicious_activity(user_id, activity_performed, suspicion_reason, performed_by=None):
    """
    Log a suspicious activity
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if performed_by is None:
            performed_by = user_id
            
        cur.execute("""
            INSERT INTO login_logs (user_id, activity_performed, performed_by, 
                                   is_suspicious, suspicion_reason, failed_attempts_count)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, activity_performed, performed_by, True, suspicion_reason, 0))
        
        conn.commit()
        cur.close()
        return True
        
    except Exception as e:
        print(f"Error logging suspicious activity: {e}")
        return False

def log_failed_login_attempt(user_id, performed_by=None):
    """
    Log a failed login attempt
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if performed_by is None:
            performed_by = user_id
            
        # Get count of recent failed attempts
        failed_count = check_failed_login_attempts(user_id)
        
        cur.execute("""
            INSERT INTO login_logs (user_id, activity_performed, performed_by, 
                                   is_suspicious, suspicion_reason, failed_attempts_count)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, 'login_failed', performed_by, failed_count >= 7, 
              f'Failed login attempt #{failed_count + 1}' if failed_count < 7 else f'Multiple failed attempts ({failed_count + 1})', 
              failed_count + 1))
        
        conn.commit()
        cur.close()
        return True
        
    except Exception as e:
        print(f"Error logging failed login attempt: {e}")
        return False
