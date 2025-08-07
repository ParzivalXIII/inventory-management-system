"""Authentication API Router for user signup and login.

This router handles:
- User registration with organization creation
- User authentication and token generation

Endpoints:
- POST /signup: Register a new user and create their organization
- POST /login: Authenticate an existing user and return an access token

Dependencies:
- SQLModel for database operations
- FastAPI for API routing
- Password hashing and verification utilities
- JWT token creation utility

Models:
- User: Represents application users
- Organization: Represents user organizations

Schemas:
- UserCreate: Input model for user creation
- Token: Response model for authentication tokens
"""

from fastapi import APIRouter, Depends, Depends, HTTPException
from sqlmodel import Session, select
from models import User, Organization
from schemas import UserCreate, Token
from auth.utils import hash_password, verify_password, create_access_token
from core.database import get_session

router = APIRouter(tags=["Auth"])

# User Signup Endpoint
@router.post("/signup", response_model=Token)
def signup(data: UserCreate, db: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = db.exec(select(User).where(User.email == data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    if not data.organization_name:
        raise HTTPException(status_code=400, detail="Organization name is required")
    
    org = Organization(name=data.organization_name)
    db.add(org)
    db.commit()
    db.refresh(org)

    if org.id is None:
        raise HTTPException(status_code=500, detail="Failed to create organization")

    # Create new user
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        organization_id=org.id,
        #organization_name=org.name,
        is_admin=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create access token
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# User Login Endpoint
@router.post("/login", response_model=Token)
def login(data: UserCreate, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}