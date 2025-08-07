import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Import models first to register them
from main import app
from core.database import get_session
from models import User, Organization, Product, Order
from auth.dependencies import get_current_user

# Test fixtures
@pytest.fixture(name="session")
def session_fixture():
    """Create a fresh database for each test"""
    engine = create_engine(
        "sqlite://",  # In-memory database
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Drop all tables (if exist) and then create all tables
    SQLModel.metadata.drop_all(engine)
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

@pytest.fixture(name="auth_client")
def auth_client_fixture(client: TestClient, session: Session):
    """Create an authenticated client with a test user"""
    # Create organization and user
    from auth.utils import hash_password
    
    org = Organization(id=1, name="TestOrg")
    session.add(org)
    session.commit()
    session.refresh(org)
    
    # Ensures the name and id fields are present in the org object
    if org.name is None:
        raise ValueError("Organization Name is empty")

    if org.id is None:
        raise ValueError("Failed to create organization")

    user = User(
        email="testuser@example.com",
        hashed_password=hash_password("password123"),
        organization_id=org.id,
        is_admin=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Mock the authentication dependency
    def get_current_user_override():
        return user
    
    app.dependency_overrides[get_current_user] = get_current_user_override
    
    return client

def test_inventory_crud_sequence(auth_client: TestClient):
    """Test complete CRUD operations for products and orders"""
    client = auth_client
    
    # Create product
    prod_resp = client.post("/products", json={
        "name": "TestProduct",
        "description": "A test product",
        "price": 12.5,
        "quantity": 50
    })
    
    print(f"Create product status: {prod_resp.status_code}")
    print(f"Create product response: {prod_resp.json()}")
    
    assert prod_resp.status_code in [200, 201]
    product_id = prod_resp.json()["id"]

    # List products
    list_resp = client.get("/products")
    assert list_resp.status_code in [200, 201]
    products = list_resp.json()
    assert any(p["id"] == product_id for p in products)

    # Update product
    update_resp = client.put(f"/products/{product_id}", json={
        "name": "UpdatedTestProduct",  # Include all fields
        "description": "An updated test product",
        "price": 15.0,
        "quantity": 45
    })
    assert update_resp.status_code in [200, 201]
    updated_product = update_resp.json()
    assert updated_product["name"] == "UpdatedTestProduct"
    assert updated_product["description"] == "An updated test product"
    assert updated_product["price"] == 15.0
    assert updated_product["quantity"] == 45

    # Delete product
    delete_resp = client.delete(f"/products/{product_id}")
    assert delete_resp.status_code in [200, 201]

    # List again - should not contain deleted product
    final_resp = client.get("/products")
    final_products = final_resp.json()
    assert all(p["id"] != product_id for p in final_products)

    # Create another product for order testing
    prod2_resp = client.post("/products", json={
        "name": "Prod2",
        "description": "Another product",
        "price": 20.0,
        "quantity": 60
    })
    prod2_id = prod2_resp.json()["id"]

    # Create an order
    order_resp = client.post("/orders", json={
        "product_id": prod2_id,
        "quantity": 2
    })
    
    print(f"Create order status: {order_resp.status_code}")
    print(f"Create order response: {order_resp.json()}")
    
    assert order_resp.status_code == 200
    assert order_resp.json()["quantity"] == 2

    # List orders
    orders_resp = client.get("/orders")
    assert orders_resp.status_code == 200
    orders = orders_resp.json()
    assert any(o["product_id"] == prod2_id for o in orders)