# This module defines API endpoints for managing products and orders in the system.
# It includes CRUD operations for products and orders, with authentication and
# authorization checks to ensure users can only access resources belonging to their organization.
# The endpoints use FastAPI's dependency injection system for database sessions and user authentication.

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import crud
from schemas import ProductCreate, ProductRead, ProductUpdate, OrderCreate, OrderRead
from models import User
from models import User
from auth.dependencies import get_current_user
from core.database import get_session

router = APIRouter(tags=["src"])

# ---------- PRODUCTS ---------- 

@router.post("/products", response_model=ProductRead)
def create_product(data: ProductCreate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Creates a new product in the database."""
    return crud.create_product(db, current_user.organization_id, data)

@router.get("/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return crud.list_products(db, current_user.organization_id)

@router.put("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Updates an existing product in the database."""
    product = crud.update_product(db, org_id=current_user.organization_id, product_id=product_id, data=data)
    if not product or product.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Deletes a product from the database."""
    product = db.get(crud.Product, product_id)
    if not product or product.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, org_id=current_user.organization_id, product_id=product_id)  # Pass org_id to delete_product(
    return {"message": "Product deleted successfully"}

# -------- ORDERS ---------

@router.post("/orders", response_model=OrderRead)
def create_order(data: OrderCreate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return crud.create_order(db, current_user.organization_id, data)

@router.get("/orders", response_model=list[OrderRead])
def read_orders(db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return crud.list_orders(db, current_user.organization_id)

@router.put("/orders/{order_id}/fulfilled", response_model=OrderRead)
def fulfill_order(order_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return crud.update_order_fulfillment_status(db, current_user.organization_id, order_id)