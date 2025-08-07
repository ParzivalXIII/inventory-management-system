"""
Database Configuration and Session Management

This script sets up the database connection and provides utilities for session management.
It uses SQLModel for ORM functionality and SQLAlchemy for database operations.

Key Components:
- DATABASE_URL: Configuration for the database connection string.
- engine: SQLAlchemy engine for database operations.
- get_session(): Context manager for database sessions.
- initialize_database(): Creates all database tables based on SQLModel definitions.
"""

from sqlmodel import SQLModel, create_engine, Session
from core.config import settings
import os

# Create the database engine using the DATABASE_URL from settings
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)

# Context manager for database sessions
def get_session():
    with Session(engine) as session:
        yield session


async def initialize_database():
    """
    Initializes the database by creating all tables defined in the SQLModel metadata.
    """
    SQLModel.metadata.create_all(engine)
