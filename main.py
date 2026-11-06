import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from auth import authenticate_user, create_access_token, get_current_user
from logger import logger

app = FastAPI(title="JwtAuthService", version="1.0.0")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MessageResponse(BaseModel):
    message: str

@app.post("/login", response_model=Token, tags=["auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and return a JWT.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.info("Login failed for %s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    logger.info("User %s logged in", user["username"])
    return Token(access_token=access_token)

@app.get("/protected", response_model=MessageResponse, tags=["protected"])
async def protected_route(current_user: dict = Depends(get_current_user)):
    """
    Example of a protected endpoint.
    """
    username = current_user["username"]
    logger.debug("Protected endpoint accessed by %s", username)
    return MessageResponse(message=f"Hello, {username}! This is a protected route.")