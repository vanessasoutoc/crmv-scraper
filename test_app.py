import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!"}

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_crmv_endpoint(client):
    response = client.get('/api/crmv/12345/MG')
    assert response.status_code == 200
    assert 'data' in response.json