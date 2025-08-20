#!/usr/bin/env python3
"""
Debug script to check password status and manually update one password
"""

import psycopg2
import hashlib

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def debug_passwords():
    """Debug password update process"""
    try:
        # Connect to database
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(
            dbname="ERP",
            user="postgres",
            password="Admin",
            host="localhost",
            port="5432"
        )
        
        cur = conn.cursor()
        print("✅ Database connected!")
        
        # Check current passwords
        print("\n🔍 Current passwords in database:")
        cur.execute("SELECT user_id, name, email, password_hash FROM users ORDER BY user_id")
        users = cur.fetchall()
        
        for user in users:
            user_id, name, email, password_hash = user
            print(f"  User {user_id}: {name} ({email}) - Password: '{password_hash}'")
        
        # Try to update one password manually
        print("\n🔄 Testing password update for first user...")
        if users:
            user_id, name, email, current_password = users[0]
            hashed_password = hash_password(current_password)
            
            print(f"  Updating user {user_id} ({name})")
            print(f"  Old password: '{current_password}'")
            print(f"  New hash: {hashed_password[:20]}...")
            
            cur.execute("UPDATE users SET password_hash = %s WHERE user_id = %s", 
                       (hashed_password, user_id))
            
            conn.commit()
            print("  ✅ Password updated successfully!")
            
            # Verify the update
            cur.execute("SELECT password_hash FROM users WHERE user_id = %s", (user_id,))
            updated_password = cur.fetchone()[0]
            print(f"  Verified hash: {updated_password[:20]}...")
        
        cur.close()
        conn.close()
        print("\n✅ Debug completed!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_passwords()
