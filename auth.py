import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config import get_settings
from utils import verify_password

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# In‑memory user store for demo purposes.
# In a real project this would be replaced by a DB model.
FAKE_USERS_DB: Dict[str, Dict[str, Any]] = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderland",
        # Password is "secret"
        "hashed_password": "$2b$12$KIX/8MZQf6Rz7YfY5xXcUuZ8QfV6w9Y1ZcKp3d0hM5i3r5GvJQm5e",
        "disabled": False,
    }
}

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Validate username and password against the user store.

    Returns the user dict if authentication succeeds, else None.
    """
    user = FAKE_USERS_DB.get(username)
    if not user:
        logger.info("Authentication failed: user %s not found", username)
        return None
    if not verify_password(password, user["hashed_password"]):
        logger.info("Authentication failed: invalid password for %s", username)
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a JWT token.

    Args:
        data: Payload data (must include a "sub" claim).
        expires_delta: Optional custom expiration.

    Returns:
        Encoded JWT as a string.
    """
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    logger.debug("Access token created for %s", data.get("sub"))
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    FastAPI dependency that extracts the current user from a JWT.

    Raises:
        HTTPException 401 if token is invalid or user does not exist.
    """
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        logger.warning("JWT decode error: %s", e)
        raise credentials_exception

    user = FAKE_USERS_DB.get(username)
    if user is None:
        raise credentials_exception
    return user