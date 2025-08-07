"""
This script defines application settings using Pydantic's BaseSettings for configuration management.
It loads settings from environment variables and a .env file (test.env), with fallback defaults.
The settings include:
- SECRET_KEY: Used for JWT token generation
- DATABASE_URL: Connection string for the database
- ALGORITHM: JWT token signing algorithm
- ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration duration

The script also verifies the existence of the .env file and prints its location and existence status.
Finally, it instantiates the Settings class to make the configuration available.
"""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env files."""
    
    SECRET_KEY: str = Field(default=os.getenv("SECRET_KEY", "citadelxiii"), description="Secret key for JWT token generation")
    DATABASE_URL: str = Field(default=os.getenv("DATABASE_URL", "sqlite:///./test.db"), description="Database connection URL")
    ALGORITHM: str = Field(default="HS256", description="Algorithm for JWT token generation")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Token expiration time in minutes")
    
    # Get the directory where this Python file is located
    # and construct the path to test.env relative to it
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / "test.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Test if the file exists before creating settings
env_file_path = Path(__file__).parent / "test.env"
print(f"Looking for env file at: {env_file_path.absolute()}")
print(f"File exists: {env_file_path.exists()}")

# Instantiate Settings
settings = Settings()