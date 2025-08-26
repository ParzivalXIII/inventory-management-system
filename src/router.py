# This module defines API endpoints for managing products and orders in the system.
# It includes CRUD operations for products and orders, with authentication and
# authorization checks to ensure users can only access resources belonging to their organization.
# The endpoints use FastAPI's dependency injection system for database sessions and user authentication.

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import crud
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import crud
from schemas import ProductCreate, ProductRead, ProductUpdate, OrderCreate, OrderRead
from models import User, Product
from auth.dependencies import get_current_user
from core.database import get_session

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter(tags=["src"])

# ---------- PRODUCTS ---------- 

@router.post("/products", response_model=ProductRead)
def create_product(data: ProductCreate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    logger.info(f"Create product initiated by user {current_user.id} from organization {current_user.organization_id}")
    product = crud.create_product(db, current_user.organization_id, data)
    logger.info(f"Product created: {product}")
    return product

@router.get("/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    logger.info(f"List products initiated by user {current_user.id} from organization {current_user.organization_id}")
    products = crud.list_products(db, current_user.organization_id)
    logger.info(f"Products listed: {[p.id for p in products]}")
    return products

@router.put("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    logger.info(f"Update product {product_id} initiated by user {current_user.id} from organization {current_user.organization_id}")
    product = crud.update_product(db, org_id=current_user.organization_id, product_id=product_id, data=data)
    if not product or product.organization_id != current_user.organization_id:
        logger.error(f"Product {product_id} not found or unauthorized access attempt by user {current_user.id}")
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info(f"Product {product_id} updated: {product}")
    return product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    logger.info(f"Delete product {product_id} initiated by user {current_user.id} from organization {current_user.organization_id}")
    product = db.get(Product, product_id)
    if not product or product.organization_id != current_user.organization_id:
        logger.error(f"Product {product_id} not found or unauthorized access attempt by user {current_user.id}")
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, org_id=current_user.organization_id, product_id=product_id)
    logger.info(f"Product {product_id} deleted successfully")
    return {"message": "Product deleted successfully"}

# -------- ORDERS ---------

@router.post("/orders", response_model=OrderRead)
def create_order(data: OrderCreate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    logger.info(f"Create order initiated by user {current_user.id} from organization {current_user.organization_id}")
    order = crud.create_order(db, current_user.organization_id, data)
    logger.info(f"Order created: {order}")
    return order

@router.get("/orders", response_model=list[OrderRead])
def read_orders(db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    logger.info(f"List orders initiated by user {current_user.id} from organization {current_user.organization_id}")
    orders = crud.list_orders(db, current_user.organization_id)
    logger.info(f"Orders listed: {[o.id for o in orders]}")
    return orders

@router.put("/orders/{order_id}/fulfilled", response_model=OrderRead)
def fulfill_order(order_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    logger.info(f"Fulfill order {order_id} initiated by user {current_user.id} from organization {current_user.organization_id}")
    order = crud.update_order_fulfillment_status(db, current_user.organization_id, order_id)
    logger.info(f"Order {order_id} fulfillment status updated: {order}")
    return order


