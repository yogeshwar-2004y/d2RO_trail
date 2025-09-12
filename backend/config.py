"""
Configuration settings for the Flask application
"""
import os
import psycopg2

class Config:
    """Base configuration class"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # File upload configuration
    UPLOAD_FOLDER = 'plan_doc_uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'xlsx', 'xls'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    # Login background configuration
    LOGIN_BACKGROUND_FOLDER = 'login_background_uploads'
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Database configuration
    DATABASE_CONFIG = {
        'dbname': "ERP",
        'user': "postgres", 
        'password': "Admin",
        'host': "localhost",
        'port': "5432"
    }

class DatabaseConnection:
    """Database connection handler"""
    
    def __init__(self):
        self.conn = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**Config.DATABASE_CONFIG)
            print("Database connection established successfully")
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            raise e
    
    def get_connection(self):
        """Get database connection"""
        if self.conn is None or self.conn.closed:
            self.connect()
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn and not self.conn.closed:
            self.conn.close()

# Global database connection instance
db_connection = DatabaseConnection()

def get_db_connection():
    """Get database connection for use in routes"""
    return db_connection.get_connection()
