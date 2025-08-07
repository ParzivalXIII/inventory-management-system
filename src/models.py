# SQLModel definitions for Organization, User, Product, and Order entities

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Organization(SQLModel, table=True):
    """Represents an organization with associated users, products, and orders.

    Attributes:
        id: Unique identifier for the organization (auto-generated primary key).
        name: Name of the organization (must be unique).
        created_at: Timestamp when the organization was created (auto-generated).
        users: List of User objects associated with this organization.
        products: List of Product objects associated with this organization.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)

    users: list["User"] = Relationship(back_populates="organization")
    #projects: list["Product"] = Relationship(back_populates="organization")

class User(SQLModel, table=True):
    """Represents a user within an organization."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    organization_id: int = Field(foreign_key="organization.id", index=True)
    #organization_name: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

    organization: Optional["Organization"] = Relationship(back_populates="users")

class Product(SQLModel, table=True):
    """Represents a product offered by an organization."""

    id: Optional[int] = Field(default=None, primary_key=True)
    organization_id: int = Field(foreign_key="organization.id", index=True)
    name: str
    description: Optional[str]
    price: float
    quantity: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)

    #organization : Optional[Organization] = Relationship(back_populates="products")
    #orders: list["Order"] = Relationship(back_populates="product")

class Order(SQLModel, table=True):
    """Represents an order placed by a customer/user for a product."""
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    organization_id: int = Field(foreign_key="organization.id", index=True)
    product_id: int = Field(foreign_key="product.id", index=True)
    quantity: int
    order_date: datetime = Field(default_factory=datetime.now)

    #product: Optional[Product] = Relationship(back_populates="orders")