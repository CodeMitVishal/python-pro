"""Sign-up and login (Module 24)."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from taskboard.deps import DB, CurrentUser
from taskboard.models import User
from taskboard.schemas import SignUp, Token, UserOut
from taskboard.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=201)
def signup(data: SignUp, db: DB) -> UserOut:
    user = User(email=data.email.lower(), password_hash=hash_password(data.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "email already registered") from None
    db.refresh(user)
    return UserOut.model_validate(user)


@router.post("/token")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB) -> Token:
    user = db.scalars(select(User).where(User.email == form.username.lower())).first()
    if user is None or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "wrong email or password", headers={"WWW-Authenticate": "Bearer"})
    return Token(access_token=create_access_token(user.id))


@router.get("/me")
def me(user: CurrentUser) -> UserOut:
    return UserOut.model_validate(user)
