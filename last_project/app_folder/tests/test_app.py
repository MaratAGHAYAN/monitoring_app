from app import app, metrics
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'System Metrics Dashboard' in response.data

def test_post_data(client):
    response = client.post('/', data={'cpu': '5', 'ram': '9'})
    assert response.status_code == 200
    assert b'Submitted Values' in response.data
    assert b'CPU: 5' in response.data
    assert b'RAM: 9' in response.data
