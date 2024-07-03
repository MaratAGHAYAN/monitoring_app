# tests/test_app.py

from flask import Flask
from flask.testing import FlaskClient
from app import app  

import pytest

@pytest.fixture
def client() -> FlaskClient:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_post_data(client):
    data = {'cpu': '5', 'ram': '9'}
    response = client.post('/', data=data)
    assert response.status_code == 200
    assert b'Submitted Values' in response.data
    
    response_str = response.data.decode('utf-8')
    
    assert f"<strong>CPU:</strong> {data['cpu']}" in response_str
    assert f"<strong>RAM:</strong> {data['ram']}" in response_str
