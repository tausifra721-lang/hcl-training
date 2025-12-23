import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307 or response.status_code == 302
    # Should redirect to /static/index.html
    assert "/static/index.html" in str(response.url)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Basketball Team/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Basketball Team" in response.json()["message"]

def test_signup_for_activity_already_signed_up():
    # Sign up first
    client.post("/activities/Art Club/signup", params={"email": "duplicate@mergington.edu"})
    # Try again
    response = client.post("/activities/Art Club/signup", params={"email": "duplicate@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
