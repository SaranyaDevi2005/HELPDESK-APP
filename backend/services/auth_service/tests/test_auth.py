import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Mock DB before importing app
with patch("database.users_col") as mock_col:
    from main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

def test_login_invalid():
    with patch("main.users_col") as mock_col:
        mock_col.find_one.return_value = None
        resp = client.post("/login", json={"username": "bad", "password": "bad"})
        assert resp.status_code == 401

def test_register_duplicate():
    with patch("main.users_col") as mock_col:
        mock_col.find_one.return_value = {"username": "existing"}
        resp = client.post("/register", json={
            "username": "existing", "password": "pass",
            "email": "a@a.com", "user_type": "user",
            "department": "IT", "role": "Developer", "employee_id": "E001"
        })
        assert resp.status_code == 400
