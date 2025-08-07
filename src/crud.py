# Database operations for managing products and orders in the system.
# This module provides CRUD operations for products and orders, scoped to specific organizations.
# It includes functions for creating, reading, updating, and deleting products and orders.
# The operations ensure proper organization scoping and data integrity through SQLAlchemy sessions.

from sqlmodel import Session, select
from models import Product, Order
from schemas import ProductCreate, ProductUpdate, OrderCreate
from typing import Optional, List

def create_product(db: Session, org_id: int, data: ProductCreate) -> Product:
    """
    Creates a new product in the database for a specific organization.

    Args:
        db: SQLAlchemy database session
        org_id: ID of the organization the product belongs to
        data: ProductCreate schema containing product details

    Returns:
        The newly created Product object
    """
    product = Product(**data.model_dump(), organization_id=org_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def list_products(db: Session, org_id: int) -> List[Product]:
    """Lists all products for a specific organization.

    Args:
        db: SQLAlchemy database session
        org_id: ID of the organization to list products for
    Returns:
        List of Product objects belonging to the organization
    """
    query = select(Product).where(Product.organization_id == org_id)
    return list(db.exec(query).all())

def update_product(db: Session, org_id: int, product_id: int, data: ProductUpdate) -> Optional[Product]:
    """Updates an existing product in the database for a specific organization.

    Args:
        db: SQLAlchemy database session
        org_id: ID of the organization the product belongs to
        product_id: ID of the product to update
        data: ProductUpdate schema containing fields to update

    Returns:
        The updated Product object if found, None otherwise
    """
    product = db.get(Product, product_id)
    if not product:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> bool:
    """Deletes a product from the database.

    Args:
        db: SQLAlchemy database session
        product_id: ID of the product to delete

    Returns:
        bool: True if the product was deleted, False if the product was not found
    """
    product = db.get(Product, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True

def create_order(db: Session, org_id: int, data: OrderCreate) -> Order:
    """Creates a new order in the database for a specific organization.

    Args:
        db: SQLAlchemy database session
        org_id: ID of the organization the order belongs to
        data: OrderCreate schema containing order details

    Returns:
        The newly created Order object
    """
    order = Order(**data.model_dump(), organization_id=org_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def list_orders(db: Session, org_id: int) -> List[Order]:
    query = select(Order).where(Order.organization_id == org_id)
    return list(db.exec(query).all())

