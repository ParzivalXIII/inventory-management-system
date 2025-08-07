# This module provides authentication utilities for FastAPI applications.
# It includes functions to validate JWT tokens and retrieve the current user from the database.
# The `get_current_user` dependency is used to authenticate and authorize requests in protected routes.

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from auth.utils import decode_token
from models import User
from core.database import get_session

# Initialize OAuth2 password bearer scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
    """Retrieves the current user from the database based on the provided JWT token.
    Raises an HTTPException if the token is invalid or the user does not exist.

    Args:
        token (str): The JWT token provided in the Authorization header.
        db (Session): The database session dependency.
    Returns:
        User: The authenticated user object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.get(User, user_id)
    if not user:
        raise credentials_exception
    return user