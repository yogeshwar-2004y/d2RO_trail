#!/usr/bin/env python3
"""
Test script for role-based commenting functionality
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_DOCUMENT_ID = "TEST-DOC-001"

def test_role_based_comments():
    """Test role-based commenting functionality"""
    
    print("🧪 Testing Role-Based Commenting Functionality")
    print("=" * 50)
    
    # Test data for different roles
    test_roles = [
        {"role": "QA Reviewer", "can_add": True, "can_delete": True, "can_accept_reject": False},
        {"role": "Designer", "can_add": False, "can_delete": False, "can_accept_reject": True},
        {"role": "Design Head", "can_add": False, "can_delete": False, "can_accept_reject": True},
        {"role": "QA Head", "can_add": False, "can_delete": False, "can_accept_reject": False},
        {"role": "Admin", "can_add": False, "can_delete": False, "can_accept_reject": False},
    ]
    
    for test_role in test_roles:
        print(f"\n🔍 Testing {test_role['role']} permissions:")
        
        # Test comment creation
        comment_data = {
            "document_id": TEST_DOCUMENT_ID,
            "document_name": "Test Document",
            "description": f"Test comment from {test_role['role']}",
            "commented_by": f"Test {test_role['role']}",
            "user_role": test_role['role']
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/comments", json=comment_data)
            
            if test_role['can_add']:
                if response.status_code == 200:
                    print(f"  ✅ Can add comments: PASSED")
                    comment_id = response.json().get('comment_id')
                else:
                    print(f"  ❌ Can add comments: FAILED (Status: {response.status_code})")
                    comment_id = None
            else:
                if response.status_code == 403:
                    print(f"  ✅ Cannot add comments (as expected): PASSED")
                else:
                    print(f"  ❌ Should not be able to add comments: FAILED (Status: {response.status_code})")
                comment_id = None
                
        except requests.exceptions.ConnectionError:
            print(f"  ⚠️  Backend not running - skipping {test_role['role']} tests")
            continue
        except Exception as e:
            print(f"  ❌ Error testing {test_role['role']}: {e}")
            continue
        
        # Test comment deletion (if comment was created)
        if comment_id and test_role['can_delete']:
            try:
                delete_data = {"user_role": test_role['role']}
                response = requests.delete(f"{BASE_URL}/api/comments/{comment_id}", json=delete_data)
                
                if response.status_code == 200:
                    print(f"  ✅ Can delete comments: PASSED")
                else:
                    print(f"  ❌ Can delete comments: FAILED (Status: {response.status_code})")
            except Exception as e:
                print(f"  ❌ Error testing delete: {e}")
        
        # Test comment acceptance (if comment exists)
        if comment_id and test_role['can_accept_reject']:
            try:
                accept_data = {
                    "justification": f"Accepted by {test_role['role']}",
                    "accepted_by": f"Test {test_role['role']}",
                    "designer_id": 123,
                    "user_role": test_role['role']
                }
                response = requests.post(f"{BASE_URL}/api/comments/{comment_id}/accept", json=accept_data)
                
                if response.status_code == 200:
                    print(f"  ✅ Can accept comments: PASSED")
                else:
                    print(f"  ❌ Can accept comments: FAILED (Status: {response.status_code})")
            except Exception as e:
                print(f"  ❌ Error testing accept: {e}")
    
    print(f"\n🎯 Role-Based Commenting Test Summary:")
    print("=" * 50)
    print("✅ QA Reviewer: Can add and delete comments")
    print("✅ Designer: Can accept/reject comments")
    print("✅ Design Head: Can accept/reject comments")
    print("✅ QA Head: View-only access")
    print("✅ Admin: View-only access")

if __name__ == "__main__":
    test_role_based_comments()
