from passlib.context import CryptContext
import logging
from typing import Optional

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.

    Args:
        password: The raw password string.

    Returns:
        A bcrypt hash.
    """
    if not password:
        raise ValueError("Password must not be empty")
    hashed = pwd_context.hash(password)
    logger.debug("Password hashed")
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its bcrypt hash.

    Args:
        plain_password: The password provided by the user.
        hashed_password: The stored bcrypt hash.

    Returns:
        True if the password matches, False otherwise.
    """
    if not plain_password or not hashed_password:
        return False
    result = pwd_context.verify(plain_password, hashed_password)
    logger.debug("Password verification result: %s", result)
    return result