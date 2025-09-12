"""
API tests for authentication endpoints
"""
import pytest
import json
from unittest.mock import patch, Mock

class TestAuthAPI:
    """Test cases for authentication API endpoints"""
    
    def test_hello_world_endpoint(self, client):
        """Test the basic hello world endpoint"""
        response = client.get('/api')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Hello from Flask!"
    
    @pytest.mark.api
    def test_login_success(self, client, mock_db_connection, sample_user_data, sample_user_db_response):
        """Test successful login"""
        mock_connection, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = sample_user_db_response
        
        with patch('routes.auth.verify_password', return_value=True):
            response = client.post('/api/login', 
                                 data=json.dumps(sample_user_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['message'] == "Login successful"
            assert 'user' in data
            assert data['user']['email'] == sample_user_data['email']
    
    @pytest.mark.api
    def test_login_missing_data(self, client):
        """Test login with missing data"""
        response = client.post('/api/login', 
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert "Email and password are required" in data['message']
    
    @pytest.mark.api
    def test_login_no_json_data(self, client):
        """Test login with no JSON data"""
        response = client.post('/api/login')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert "No data provided" in data['message']
    
    @pytest.mark.api
    def test_login_invalid_password(self, client, mock_db_connection, sample_user_data, sample_user_db_response):
        """Test login with invalid password"""
        mock_connection, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = sample_user_db_response
        
        with patch('routes.auth.verify_password', return_value=False):
            response = client.post('/api/login', 
                                 data=json.dumps(sample_user_data),
                                 content_type='application/json')
            
            assert response.status_code == 401
            data = json.loads(response.data)
            assert data['success'] is False
            assert "Invalid password" in data['message']
    
    @pytest.mark.api
    def test_login_user_not_found(self, client, mock_db_connection, sample_user_data):
        """Test login with non-existent user"""
        mock_connection, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = None
        
        response = client.post('/api/login', 
                             data=json.dumps(sample_user_data),
                             content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert "User not found" in data['message']
    
    @pytest.mark.api
    def test_login_database_error(self, client, sample_user_data):
        """Test login with database connection error"""
        with patch('config.get_db_connection', side_effect=Exception("Database connection failed")):
            response = client.post('/api/login', 
                                 data=json.dumps(sample_user_data),
                                 content_type='application/json')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['success'] is False
            assert "Internal server error" in data['message']
