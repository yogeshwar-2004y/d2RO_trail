#!/usr/bin/env python3
"""
Script to update existing passwords to use proper hashing
"""

import psycopg2
import hashlib

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def update_passwords():
    """Update existing passwords to use proper hashing"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            dbname="ERP",
            user="postgres",
            password="Admin",
            host="localhost",
            port="5432"
        )
        
        cur = conn.cursor()
        
        # Get all users with their current passwords
        cur.execute("SELECT user_id, password_hash FROM users")
        users = cur.fetchall()
        
        print("🔄 Updating passwords to use proper hashing...")
        
        for user_id, current_password in users:
            # Hash the current password
            hashed_password = hash_password(current_password)
            
            # Update the user's password
            cur.execute("UPDATE users SET password_hash = %s WHERE user_id = %s", 
                       (hashed_password, user_id))
            
            print(f"  ✅ Updated user {user_id}: {current_password} → {hashed_password[:10]}...")
        
        # Commit the changes
        conn.commit()
        print("✅ All passwords updated successfully!")
        
        # Verify the update
        print("\n🔍 Verifying updated passwords...")
        cur.execute("SELECT user_id, password_hash FROM users")
        updated_users = cur.fetchall()
        
        for user_id, hashed_password in updated_users:
            print(f"  - User {user_id}: {hashed_password[:10]}...")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error updating passwords: {str(e)}")

if __name__ == "__main__":
    update_passwords()
