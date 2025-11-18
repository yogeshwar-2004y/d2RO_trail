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
    
    # Signature upload configuration
    SIGNATURE_UPLOAD_FOLDER = 'signature_uploads'
    ALLOWED_SIGNATURE_EXTENSIONS = {'png'}
    MAX_SIGNATURE_SIZE = 5 * 1024 * 1024  # 5MB
    
    # Database configuration
    DATABASE_CONFIG = {
        'dbname': "ERP",
        'user': "postgres", 
        'password': "Mahadev@2004",
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
            # Close existing connection if it exists
            if self.conn and not self.conn.closed:
                try:
                    self.conn.close()
                except:
                    pass
            self.conn = psycopg2.connect(**Config.DATABASE_CONFIG)
            print("Database connection established successfully")
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            raise e
    
    def get_connection(self):
        """Get database connection - reconnect if closed or stale"""
        try:
            # Check if connection exists and is valid
            if self.conn is None or self.conn.closed:
                self.connect()
            else:
                # Test connection with a simple query
                try:
                    cur = self.conn.cursor()
                    cur.execute("SELECT 1")
                    cur.fetchone()
                    cur.close()
                except (psycopg2.OperationalError, psycopg2.InterfaceError):
                    # Connection is stale, reconnect
                    print("Database connection is stale, reconnecting...")
                    self.connect()
        except Exception as e:
            print(f"Error checking database connection: {str(e)}")
            # Try to reconnect
            try:
                self.connect()
            except:
                raise e
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
