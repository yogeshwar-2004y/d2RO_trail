"""
Main Flask application with modular structure using blueprints
"""
from flask import Flask
from flask_cors import CORS

# Import configuration and utilities
from config import Config
from utils.helpers import create_upload_directories
from utils.database_init import initialize_database

# Import all blueprints
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.users import users_bp
from routes.documents import documents_bp
from routes.tests import tests_bp
from routes.news import news_bp
from routes.files import files_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Create upload directories
    create_upload_directories()
    
    # Initialize database
    initialize_database()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(tests_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(files_bp)
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
