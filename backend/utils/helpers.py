"""
Utility functions for the Flask application
"""
import hashlib
import os
from config import Config

def allowed_file(filename):
    """Check if file extension is allowed for document uploads"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def allowed_image_file(filename):
    """Check if file extension is allowed for image uploads"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_IMAGE_EXTENSIONS

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash"""
    # return hash_password(password) == hashed_password
    return password == hashed_password

def create_upload_directories():
    """Create upload directories if they don't exist"""
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.LOGIN_BACKGROUND_FOLDER, exist_ok=True)

def validate_file_size(file, max_size):
    """Validate file size"""
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    return file_size <= max_size

def handle_database_error(conn, error_message="Database error"):
    """Handle database errors with rollback"""
    try:
        conn.rollback()
    except:
        pass
    print(f"Database error: {error_message}")
    return {"success": False, "message": f"Database error: {error_message}"}, 500
