"""
Unit tests for configuration module
"""
import pytest
from unittest.mock import patch, Mock
from config import Config, DatabaseConnection, get_db_connection

class TestConfig:
    """Test cases for Config class"""
    
    def test_config_default_values(self):
        """Test that Config has expected default values"""
        assert Config.DEBUG is True
        assert Config.SECRET_KEY is not None
        assert 'pdf' in Config.ALLOWED_EXTENSIONS
        assert 'docx' in Config.ALLOWED_EXTENSIONS
        assert Config.MAX_FILE_SIZE == 50 * 1024 * 1024
        assert Config.MAX_IMAGE_SIZE == 10 * 1024 * 1024
    
    def test_database_config_structure(self):
        """Test that database configuration has required fields"""
        db_config = Config.DATABASE_CONFIG
        required_fields = ['dbname', 'user', 'password', 'host', 'port']
        
        for field in required_fields:
            assert field in db_config
            assert db_config[field] is not None

class TestDatabaseConnection:
    """Test cases for DatabaseConnection class"""
    
    @patch('psycopg2.connect')
    def test_database_connection_success(self, mock_connect):
        """Test successful database connection"""
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        
        db_conn = DatabaseConnection()
        
        assert db_conn.conn is not None
        mock_connect.assert_called_once_with(**Config.DATABASE_CONFIG)
    
    @patch('psycopg2.connect')
    def test_database_connection_failure(self, mock_connect):
        """Test database connection failure"""
        mock_connect.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception) as exc_info:
            DatabaseConnection()
        
        assert "Connection failed" in str(exc_info.value)
    
    @patch('psycopg2.connect')
    def test_get_connection_when_closed(self, mock_connect):
        """Test getting connection when it's closed"""
        mock_conn = Mock()
        mock_conn.closed = 1  # psycopg2 closed status
        mock_connect.return_value = mock_conn
        
        db_conn = DatabaseConnection()
        db_conn.conn = mock_conn
        
        # Should reconnect when connection is closed
        result = db_conn.get_connection()
        
        assert mock_connect.call_count == 2  # Initial connection + reconnection
    
    @patch('psycopg2.connect')
    def test_close_connection(self, mock_connect):
        """Test closing database connection"""
        mock_conn = Mock()
        mock_conn.closed = 0  # psycopg2 open status
        mock_connect.return_value = mock_conn
        
        db_conn = DatabaseConnection()
        db_conn.close()
        
        mock_conn.close.assert_called_once()

class TestGetDbConnection:
    """Test cases for get_db_connection function"""
    
    @patch('config.db_connection')
    def test_get_db_connection(self, mock_db_connection):
        """Test get_db_connection function"""
        mock_connection = Mock()
        mock_db_connection.get_connection.return_value = mock_connection
        
        result = get_db_connection()
        
        assert result == mock_connection
        mock_db_connection.get_connection.assert_called_once()
