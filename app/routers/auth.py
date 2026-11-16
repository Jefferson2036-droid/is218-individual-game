"""Accounts: register, log in, log out, and "who am I"."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..config import settings
from ..deps import COOKIE_NAME, get_current_user, get_db
from ..models import User
from ..schemas import LoginIn, RegisterIn
from ..security import create_token, hash_password, verify_password
from ..views import user_out

router = APIRouter(prefix="/api", tags=["accounts"])

# Checked when the email is unknown, so a wrong email takes as long as a wrong password.
_DUMMY_HASH = hash_password("not-a-real-password")

EMAIL_TAKEN = "An account with this email already exists"


def _sign_in(response: Response, user: User) -> str:
    token = create_token(user.id, settings.secret_key, settings.token_minutes)
    response.set_cookie(
        COOKIE_NAME,
        token,
        max_age=settings.token_minutes * 60,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
    )
    return token


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterIn, response: Response, db: Session = Depends(get_db)):
    email = data.email.lower()
    if db.scalar(select(User).where(User.email == email)) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, EMAIL_TAKEN)
    user = User(email=email, password_hash=hash_password(data.password), display_name=data.display_name)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, EMAIL_TAKEN)
    db.refresh(user)
    token = _sign_in(response, user)
    return {"user": user_out(user), "access_token": token, "token_type": "bearer"}


@router.post("/auth/login")
def login(data: LoginIn, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email.lower()))
    password_ok = verify_password(data.password, user.password_hash if user else _DUMMY_HASH)
    if user is None or not password_ok:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong email or password")
    token = _sign_in(response, user)
    return {"user": user_out(user), "access_token": token, "token_type": "bearer"}


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME)


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"user": user_out(user)}
