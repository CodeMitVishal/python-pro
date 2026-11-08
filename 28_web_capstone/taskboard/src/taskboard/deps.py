"""Reusable dependencies: database session and the logged-in user (Module 22, 24)."""
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from taskboard.db import get_db
from taskboard.models import User
from taskboard.security import read_user_id

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

DB = Annotated[Session, Depends(get_db)]


def current_user(db: DB, token: Annotated[str, Depends(oauth2)]) -> User:
    user_id = read_user_id(token)
    user = db.get(User, user_id) if user_id is not None else None
    if user is None:
        raise HTTPException(401, "invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    return user


CurrentUser = Annotated[User, Depends(current_user)]
