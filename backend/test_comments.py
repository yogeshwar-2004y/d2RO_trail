#!/usr/bin/env python3
"""
Test script for the comments and annotations API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_comments_api():
    """Test the comments and annotations API endpoints"""
    
    print("🧪 Testing Comments and Annotations API")
    print("=" * 50)
    
    # Test data
    test_comment = {
        "document_id": "TEST_DOC_001",
        "document_name": "test_document.pdf",
        "version": "1.0",
        "reviewer_id": 1001,
        "page_no": 1,
        "section": "Introduction",
        "description": "This is a test comment",
        "author": "Test User",
        "is_annotation": False
    }
    
    test_annotation = {
        "document_id": "TEST_DOC_001",
        "document_name": "test_document.pdf",
        "version": "1.0",
        "reviewer_id": 1001,
        "page_no": 1,
        "section": "Introduction",
        "description": "This is a test annotation",
        "author": "Test User",
        "is_annotation": True,
        "x": 50.5,
        "y": 30.2
    }
    
    try:
        # Test 1: Create a regular comment
        print("1. Creating a regular comment...")
        response = requests.post(f"{BASE_URL}/api/comments", json=test_comment)
        if response.status_code == 200:
            print("✅ Regular comment created successfully")
            comment_data = response.json()
            print(f"   Comment ID: {comment_data.get('comment_id')}")
        else:
            print(f"❌ Failed to create comment: {response.status_code}")
            print(f"   Response: {response.text}")
            return
        
        # Test 2: Create an annotation
        print("\n2. Creating an annotation...")
        response = requests.post(f"{BASE_URL}/api/comments", json=test_annotation)
        if response.status_code == 200:
            print("✅ Annotation created successfully")
            annotation_data = response.json()
            print(f"   Comment ID: {annotation_data.get('comment_id')}")
        else:
            print(f"❌ Failed to create annotation: {response.status_code}")
            print(f"   Response: {response.text}")
            return
        
        # Test 3: Get all comments for the document
        print("\n3. Retrieving comments for document...")
        response = requests.get(f"{BASE_URL}/api/comments?document_id=TEST_DOC_001")
        if response.status_code == 200:
            data = response.json()
            print("✅ Comments retrieved successfully")
            print(f"   Comments count: {len(data.get('comments', []))}")
            print(f"   Annotations count: {len(data.get('annotations', []))}")
            
            # Display comments
            for comment in data.get('comments', []):
                print(f"   - {comment['description']} by {comment['author']} ({'Annotation' if comment['annotation'] else 'Comment'})")
        else:
            print(f"❌ Failed to retrieve comments: {response.status_code}")
            print(f"   Response: {response.text}")
            return
        
        print("\n🎉 All tests passed! The comments and annotations API is working correctly.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the backend server.")
        print("   Make sure the Flask server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    test_comments_api()
