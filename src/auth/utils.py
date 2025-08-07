# Authentication Utilities Module
# This module provides functions for password hashing, verification, and JWT token creation/decoding.
# It uses bcrypt for password hashing and PyJWT for JWT operations.
# Configuration settings are loaded from the application's settings module.

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from core.config import settings

# Load configuration settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Initialize password context for hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a plain text password using bcrypt algorithm.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password string.
    """
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verifies if a plain text password matches a hashed password.

    Args:
        plain (str): The plain text password to be verified.
        hashed (str): The hashed password to compare against.

    Returns:
        bool: True if the plain text password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creates a JWT access token with the given data and expiration time.

    Args:
        data (dict): The data to be encoded in the JWT token.
        expires_delta (timedelta | None, optional): The time duration for which the token will be valid.
            If not provided, a default of 15 minutes will be used.

    Returns:
        str: The encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    """Decodes a JWT token and returns the payload data.

    Args:
        token (str): The JWT token to be decoded.

    Returns:
        dict: The decoded payload data from the JWT token.

    Raises:
        JWTError: If the token is invalid, expired, or cannot be decoded.
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
