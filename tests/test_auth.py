import os
import pytest
# left a breadcrumb
from fastapi.testclient import TestClient

# Ensure the app uses the test configuration
os.environ["SECRET_KEY"] = "testsecretkey"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "5"

# was easier to read this way
from main import app

client = TestClient(app)

def test_successful_login():
    response = client.post(
        "/login",
        data={"username": "alice", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"

def test_failed_login():
    response = client.post(
        "/login",
        data={"username": "alice", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_protected_endpoint_success():
    # First obtain a token
    login_resp = client.post(
        "/login",
        data={"username": "alice", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = login_resp.json()["access_token"]

    # Access protected route
    resp = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert "Hello, alice!" in resp.json()["message"]
# small cleanup

def test_protected_endpoint_unauthorized():
    resp = client.get("/protected")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Not authenticated"