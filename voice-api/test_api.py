#!/usr/bin/env python3
"""
Test script for Let's Talk API endpoints using Flask test client
"""
import pytest
import json
from app import app

class TestAPIEndpoints:
    """Test class for API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'healthy'
    
    def test_otp_generation(self, client):
        """Test OTP generation endpoint"""
        # First create an API token
        token_response = client.post('/api/tokens', json={
            "user_id": "test_user",
            "scopes": ["read", "write"]
        })
        assert token_response.status_code == 201
        token_data = token_response.get_json()
        token = token_data['token']
        
        # Test OTP generation with token
        response = client.post('/calls/otp', 
                             json={"phone_number": "+256700123456"},
                             headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
    
    def test_api_token_creation(self, client):
        """Test API token creation"""
        response = client.post('/api/tokens', json={
            "user_id": "test_user",
            "scopes": ["read", "write"]
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'token' in data
        assert 'id' in data
        assert data['user_id'] == 'test_user'