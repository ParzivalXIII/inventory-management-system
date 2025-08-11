# Pydantic models for API request/response schemas

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class OrgCreate(BaseModel):
    """Schema for creating an organization."""
    name: str

class UserCreate(BaseModel):
    """Schema for creating a user."""
    email: str
    password: str
    organization_name: Optional[str] = None

class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"

class ProductCreate(BaseModel):
    """Schema for creating a product."""
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    created_at: Optional[datetime] = None

class ProductRead(ProductCreate):
    """Schema for reading a product."""
    id: int
    organization_id: int

class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]

class OrderCreate(BaseModel):
    """Schema for creating an order."""
    product_id: int
    quantity: int
    order_date: Optional[datetime] = None
    total_price: Optional[float] = None
    is_fulfilled: bool = False

class OrderRead(BaseModel):
    """Schema for reading an order."""
    id: int
    product_id: int
    organization_id: int
    quantity: int
    order_date: datetime
    total_price: float
    is_fulfilled: bool

class SaleTimeSeries(BaseModel):
    """Schema for time series data of sales."""
    timestamps: List[datetime]
    total: List[int]

class HistogramOutput(BaseModel):
    """Schema for histogram data."""
    bins: List[float]
    counts: List[int]