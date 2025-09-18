"""
Pytest configuration and fixtures for the Flask application tests
"""
import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from app import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    
    # Configure for testing
    app.config.update({
        "TESTING": True,
        "DEBUG": False,
        "SECRET_KEY": "test-secret-key",
        # Use a test database configuration
        "DATABASE_CONFIG": {
            'dbname': "test_erp",
            'user': "postgres", 
            'password': "Admin",
            'host': "localhost",
            'port': "5432"
        }
    })
    
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def mock_db_connection():
    """Mock database connection for tests that don't need a real database."""
    with patch('config.get_db_connection') as mock_conn:
        mock_cursor = Mock()
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection
        yield mock_connection, mock_cursor

@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }

@pytest.fixture
def sample_user_db_response():
    """Sample database response for user login."""
    return (
        1001,  # user_id
        "Test User",  # name
        "test@example.com",  # email
        "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdCOKi8LzGDaIy6",  # password_hash
        1,     # role_id
        "admin"  # role_name
    )

@pytest.fixture
def mock_verify_password():
    """Mock password verification function."""
    with patch('routes.auth.verify_password') as mock_verify:
        mock_verify.return_value = True
        yield mock_verify
