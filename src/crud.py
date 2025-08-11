# Database operations for managing products and orders in the system.
# This module provides CRUD operations for products and orders, scoped to specific organizations.
# It includes functions for creating, reading, updating, and deleting products and orders.
# The operations ensure proper organization scoping and data integrity through SQLAlchemy sessions.

from typing import Optional, List
from sqlmodel import Session, select
from models import Product, Order
from schemas import ProductCreate, ProductUpdate, OrderCreate


def create_product(db: Session, org_id: int, data: ProductCreate) -> Product:
    """
    Creates a new product in the database for a specific organization.

    Args:
        db (Session): SQLAlchemy database session
        org_id (int): ID of the organization the product belongs to
        data (ProductCreate): ProductCreate schema containing product details

    Returns:
        Product: The newly created Product object
    """
    product = Product(**data.model_dump(), organization_id=org_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(db: Session, org_id: int) -> List[Product]:
    """
    Lists all products for a specific organization.
    Args:
        db (Session): SQLAlchemy database session
        org_id (int): ID of the organization to list products for
    Returns:
        List[Product]: List of Product objects belonging to the organization
    """
    query = select(Product).where(Product.organization_id == org_id)
    return list(db.exec(query).all())


def update_product(db: Session, org_id: int, product_id: int, data: ProductUpdate) -> Optional[Product]:
    """
    Updates an existing product in the database for a specific organization.

    Args:
        db (Session): SQLAlchemy database session
        org_id (int): ID of the organization the product belongs to
        product_id (int): ID of the product to update
        data (ProductUpdate): ProductUpdate schema containing fields to update

    Returns:
        Optional[Product]: The updated Product object if found, None otherwise
    """
    product = db.get(Product, product_id)
    if not product or product.organization_id != org_id:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, org_id: int, product_id: int) -> bool:
    """
    Deletes a product from the database.

    Args:
        db (Session): SQLAlchemy database session
        org_id (int): ID of the organization the product belongs to
        product_id (int): ID of the product to delete

    Returns:
        bool: True if the product was deleted, False if the product was not found
    """
    product = db.get(Product, product_id)
    if not product or product.organization_id != org_id:
        return False
    db.delete(product)
    db.commit()
    return True


def create_order(db: Session, org_id: int, data: OrderCreate) -> Order:
    """
    Creates a new order in the database for a specific organization.

    Args:
        db (Session): SQLAlchemy database session
        org_id (int): ID of the organization the order belongs to
        data (OrderCreate): OrderCreate schema containing order details

    Returns:
        Order: The newly created Order object
    """
    order = Order(**data.model_dump(), organization_id=org_id)
    product = db.get(Product, data.product_id)

    if not product or product.organization_id != org_id:
        raise ValueError("Product not found or does not belong to the organization.")

    if product.quantity is not None and product.quantity >= order.quantity:
        order.is_fulfilled = True
        product.quantity -= order.quantity
        db.add(product)
    else:
        order.is_fulfilled = False
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def list_orders(db: Session, org_id: int) -> List[Order]:
    """
    Lists all orders for a specific organization.

    Args:
        db (Session): SQLAlchemy database session
        org_id (int): ID of the organization to list orders for

    Returns:
        List[Order]: List of Order objects belonging to the organization
    """
    query = select(Order).where(Order.organization_id == org_id)
    return list(db.exec(query).all())

def get_order(db: Session, org_id: int, order_id: int) -> Order:
    """Retrieves a specific order by ID for a specific organization."""
    
    query = select(Order).where(Order.organization_id == org_id, Order.id == order_id)
    order = db.exec(query).first()
    if not order:
        raise ValueError(f"Order not found")
    return order

def update_order_fulfillment_status(db: Session, org_id: int, order_id: int) -> Optional[Order]:
    """
    Updates the fulfillment status of an existing order in the database for a specific organization.

    Args:
        db (Session): SQLAlchemy database session
        org_id (int): ID of the organization the order belongs to
        order_id (int): ID of the order to update

    Returns:
        Optional[Order]: The updated Order object if found, None otherwise
    """
    order = db.get(Order, order_id)
    if not order or order.organization_id != org_id:
        return None

    product = db.get(Product, order.product_id)
    if not product or product.organization_id != org_id:
        return None

    if product.quantity is not None and product.quantity >= order.quantity:
        order.is_fulfilled = True
        product.quantity -= order.quantity
        db.add(product)
    else:
        order.is_fulfilled = False

    db.add(order)
    db.commit()
    db.refresh(order)
    return order

