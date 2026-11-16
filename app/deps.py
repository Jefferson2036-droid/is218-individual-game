"""Shared request dependencies: database session, random numbers, signed-in user."""

import random

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from .config import settings
from .db import SessionLocal
from .models import User
from .security import read_token

COOKIE_NAME = "arena_session"

_rng = random.SystemRandom()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_rng():
    """The computer opponent's source of randomness (replaced in tests)."""
    return _rng


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    header = request.headers.get("Authorization", "")
    if header.lower().startswith("bearer "):
        token = header[7:].strip()
    else:
        token = request.cookies.get(COOKIE_NAME)
    user_id = read_token(token, settings.secret_key) if token else None
    user = db.get(User, user_id) if user_id is not None else None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not signed in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
