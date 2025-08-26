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
import logging
from sqlmodel import Session, select
from models import User, Organization
from schemas import UserCreate, Token
from auth.utils import hash_password, verify_password, create_access_token
from core.database import get_session

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Auth"])

# User Signup Endpoint
@router.post("/signup", response_model=Token)
def signup(data: UserCreate, db: Session = Depends(get_session)):
    logger.info(f"Signup request received for email: {data.email}")

    # Check if user already exists
    existing_user = db.exec(select(User).where(User.email == data.email)).first()
    if existing_user:
        logger.warning(f"User with email {data.email} already exists")
        raise HTTPException(status_code=400, detail="User already exists")

    if not data.organization_name:
        logger.warning("Organization name is missing in the signup request")
        raise HTTPException(status_code=400, detail="Organization name is required")
    
    logger.info(f"Creating organization: {data.organization_name}")
    org = Organization(name=data.organization_name)
    db.add(org)
    db.commit()
    db.refresh(org)

    if org.id is None:
        logger.error("Failed to create organization")
        raise HTTPException(status_code=500, detail="Failed to create organization")

    logger.info(f"Organization created with ID: {org.id}")

    # Create new user
    logger.info(f"Creating user with email: {data.email}")
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        organization_id=org.id,
        is_admin=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"User created with ID: {user.id}")

    # Create access token
    token = create_access_token({"sub": str(user.id)})
    logger.info(f"Access token generated for user: {user.id}")

    return {"access_token": token, "token_type": "bearer"}

# User Login Endpoint
@router.post("/login", response_model=Token)
def login(data: UserCreate, db: Session = Depends(get_session)):
    logger.info(f"Login request received for email: {data.email}")

    user = db.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.hashed_password):
        logger.warning(f"Invalid login attempt for email: {data.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logger.info(f"User authenticated: {user.id}")

    # Create access token
    token = create_access_token({"sub": str(user.id)})
    logger.info(f"Access token generated for user: {user.id}")

    return {"access_token": token, "token_type": "bearer"}

