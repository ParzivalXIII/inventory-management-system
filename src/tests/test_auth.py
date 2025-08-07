import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# CRITICAL: Import models BEFORE creating the engine/tables
from main import app
from core.database import get_session
from models import User, Organization  # This registers models with SQLModel.metadata

# Create in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    """Create a fresh database for each test"""
    engine = create_engine(
        "sqlite://",  # In-memory database
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables - models are already registered due to imports above
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with overridden database dependency"""
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_signup_and_login_flow(client: TestClient):
    """Test user signup and login flow with isolated database"""
    # Test signup
    signup_resp = client.post("/signup", json={
        "email": "test@example.com",
        "password": "secret",
        "organization_name": "Test Org"  
    })
    
    print(f"Signup status: {signup_resp.status_code}")
    print(f"Signup response: {signup_resp.json()}")
    
    assert signup_resp.status_code in [200, 201]
    signup_data = signup_resp.json()
    assert "access_token" in signup_data
    assert "token_type" in signup_data

    # Test login with same credentials
    login_resp = client.post("/login", json={
        "email": "test@example.com",
        "password": "secret"
    })

    print(f"Login status: {login_resp.status_code}")
    print(f"Login response: {login_resp.json()}")
    
    assert login_resp.status_code in [200, 201]
    login_data = login_resp.json()
    assert "access_token" in login_data
    assert "token_type" in login_data

def test_signup_duplicate_email(client: TestClient):
    """Test that duplicate email signup fails"""
    # First signup
    client.post("/signup", json={
        "email": "duplicate@example.com",
        "password": "secret",
        "organization_name": "Test Org"
    })
    
    # Second signup with same email should fail
    resp = client.post("/signup", json={
        "email": "duplicate@example.com",
        "password": "different",
        "organization_name": "Another Org"
    })
    
    assert resp.status_code == 400
    assert "User already exists" in resp.json()["detail"]

def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    resp = client.post("/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    
    assert resp.status_code == 401
    assert "Invalid credentials" in resp.json()["detail"]

def test_signup_missing_organization(client: TestClient):
    """Test signup without organization name"""
    resp = client.post("/signup", json={
        "email": "test@example.com",
        "password": "secret"
        # Missing organization_name
    })
    
    # Should fail with validation error or bad request
    assert resp.status_code in [400, 422]