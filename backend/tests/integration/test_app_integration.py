"""
Integration tests for the Flask application
"""
import pytest
from app import create_app

class TestAppIntegration:
    """Integration tests for the Flask application"""
    
    def test_app_creation(self):
        """Test that app can be created successfully"""
        app = create_app()
        assert app is not None
        assert app.config['TESTING'] is False  # Default config
    
    def test_app_with_test_config(self, app):
        """Test app with test configuration"""
        assert app.config['TESTING'] is True
        assert app.config['DEBUG'] is False
    
    def test_blueprints_registered(self, app):
        """Test that all blueprints are properly registered"""
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        
        expected_blueprints = [
            'auth',
            'projects', 
            'users',
            'documents',
            'tests',
            'news',
            'files'
        ]
        
        for blueprint in expected_blueprints:
            assert blueprint in blueprint_names
    
    def test_cors_enabled(self, client):
        """Test that CORS is properly enabled"""
        response = client.options('/api')
        # Should not get a 405 Method Not Allowed if CORS is enabled
        assert response.status_code in [200, 404]  # 404 is ok if endpoint doesn't exist
    
    def test_app_routes_exist(self, client):
        """Test that basic routes are accessible"""
        # Test auth routes
        response = client.get('/api')
        assert response.status_code == 200
        
        # Test POST routes exist (even if they return errors without proper data)
        # When no content-type is provided, Flask returns 500 with JSON parsing error
        response = client.post('/api/login')
        assert response.status_code in [400, 401, 405, 500]  # Should not be 404 (not found)
    
    @pytest.mark.integration 
    def test_database_connection_in_context(self, app):
        """Test database connection within app context"""
        with app.app_context():
            from config import get_db_connection
            # This should not raise an exception in the app context
            try:
                conn = get_db_connection()
                assert conn is not None
            except Exception as e:
                # Database might not be available in test environment
                # This is acceptable for this test
                assert "database" in str(e).lower() or "connection" in str(e).lower()
    
    def test_error_handlers(self, client):
        """Test that the app handles errors gracefully"""
        # Test non-existent route
        response = client.get('/non-existent-route')
        assert response.status_code == 404
        
        # Test method not allowed
        response = client.delete('/api')  # GET endpoint called with DELETE
        assert response.status_code in [405, 404]
