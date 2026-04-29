import pytest
from main import app

# This creates a "fake" web browser we can use to test your app without running a server
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test 1: Check if the main page works
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

# Test 2: Check if the health page works
def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200