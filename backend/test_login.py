#!/usr/bin/env python3
"""
Test script to verify login functionality and role fetching
"""

import psycopg2
import json

def test_database_connection():
    """Test database connection and role fetching"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            dbname="ERP",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432"
        )
        
        cur = conn.cursor()
        
        # Test the login query
        test_email = "avanthikapg22@gmail.com"
        
        cur.execute("""
            SELECT u.user_id, u.name, u.email, u.password_hash, r.role_name
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            WHERE u.email = %s
        """, (test_email,))
        
        user = cur.fetchone()
        
        if user:
            print("✅ Database connection successful!")
            print(f"User found: {user[1]} ({user[2]})")
            print(f"Role: {user[4]}")
            print(f"Password hash: {user[3]}")
            
            # Test all users and their roles
            print("\n📋 All users and their roles:")
            cur.execute("""
                SELECT u.name, u.email, r.role_name
                FROM users u
                JOIN user_roles ur ON u.user_id = ur.user_id
                JOIN roles r ON ur.role_id = r.role_id
                ORDER BY u.name
            """)
            
            users = cur.fetchall()
            for user in users:
                print(f"  - {user[0]} ({user[1]}) → {user[2]}")
                
        else:
            print("❌ User not found")
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")

if __name__ == "__main__":
    test_database_connection()
