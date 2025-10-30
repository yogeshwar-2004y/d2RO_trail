#!/usr/bin/env python3
"""
Test script to verify notification functionality
"""
from config import get_db_connection
from utils.activity_logger import get_users_by_role, log_notification

def test_notifications():
    """Test the notification system"""
    print("🧪 Testing Notification Feature")
    print("=" * 50)
    
    # Test 1: Get Design Head users
    print("\n1. Testing get_users_by_role for Design Head (role_id=4)...")
    design_heads = get_users_by_role(4)
    print(f"   Found {len(design_heads)} Design Head(s)")
    for user in design_heads:
        print(f"   - User ID: {user['user_id']}, Name: {user['name']}, Email: {user['email']}")
    
    # Test 2: Get QA Head users
    print("\n2. Testing get_users_by_role for QA Head (role_id=2)...")
    qa_heads = get_users_by_role(2)
    print(f"   Found {len(qa_heads)} QA Head(s)")
    for user in qa_heads:
        print(f"   - User ID: {user['user_id']}, Name: {user['name']}, Email: {user['email']}")
    
    # Test 3: Check if activity_logs table has notification columns
    print("\n3. Checking activity_logs table structure...")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if notification columns exist
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'activity_logs' 
            AND column_name IN ('notified_user_id', 'is_read', 'notification_type')
            ORDER BY column_name
        """)
        
        columns = cur.fetchall()
        if columns:
            print("   ✅ Notification columns found:")
            for col in columns:
                print(f"      - {col[0]}: {col[1]}")
        else:
            print("   ❌ Notification columns NOT found")
            print("   Please run the migration: python run_notifications_migration.py")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error checking table structure: {str(e)}")
    
    # Test 4: Get existing notifications for Design Head
    if design_heads:
        print("\n4. Checking existing notifications for Design Head...")
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT COUNT(*) 
                FROM activity_logs 
                WHERE notified_user_id = %s
            """, (design_heads[0]['user_id'],))
            
            count = cur.fetchone()[0]
            print(f"   Found {count} notification(s) for Design Head (user_id={design_heads[0]['user_id']})")
            
            # Show recent notifications
            cur.execute("""
                SELECT al.activity_id, al.project_id, al.activity_performed, 
                       al.timestamp, al.is_read, al.notification_type,
                       p.project_name
                FROM activity_logs al
                LEFT JOIN projects p ON al.project_id = p.project_id
                WHERE al.notified_user_id = %s
                ORDER BY al.timestamp DESC
                LIMIT 5
            """, (design_heads[0]['user_id'],))
            
            notifications = cur.fetchall()
            if notifications:
                print("\n   Recent notifications:")
                for notif in notifications:
                    read_status = "✓ Read" if notif[4] else "✗ Unread"
                    print(f"      [{notif[0]}] {notif[2]} - Project: {notif[6] or 'N/A'} ({read_status})")
                    print(f"          Time: {notif[3]}")
            else:
                print("   No notifications yet")
            
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"   ❌ Error checking notifications: {str(e)}")
    
    # Test 5: Get unread count for each role
    print("\n5. Checking unread notification counts...")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        for role_name, role_id in [("QA Head", 2), ("Design Head", 4)]:
            users = get_users_by_role(role_id)
            for user in users:
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM activity_logs 
                    WHERE notified_user_id = %s AND is_read = FALSE
                """, (user['user_id'],))
                
                unread_count = cur.fetchone()[0]
                print(f"   {role_name} ({user['name']}): {unread_count} unread notification(s)")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error checking unread counts: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Notification system test completed!")
    print("\nNext steps:")
    print("1. Create a project using the admin interface")
    print("2. Check notifications for Design Head and QA Head")
    print("3. Implement frontend notification display")

if __name__ == "__main__":
    test_notifications()

