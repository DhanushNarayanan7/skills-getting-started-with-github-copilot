import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data
    assert "participants" in data["Soccer Team"]

def test_signup_and_duplicate():
    # Use a unique email for testing
    test_email = "testuser@mergington.edu"
    activity = "Soccer Team"
    # First signup should succeed
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
