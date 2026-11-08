"""pydantic models: what clients send and what we send back (Module 22)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from taskboard.models import Status


class SignUp(BaseModel):
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", max_length=200)
    password: str = Field(min_length=10)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    is_admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    status: Status | None = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    status: Status
    owner_id: int
    created_at: datetime


class Page(BaseModel):
    total: int
    items: list[TaskOut]
