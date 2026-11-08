"""Module 22 · pydantic: validate data at the edges of your app

Every byte that comes from outside (JSON bodies, query strings, env vars, files)
is untrusted. pydantic turns it into typed Python objects, or explains exactly
what's wrong. FastAPI uses it for every request and response.

Run it:  python 22_fastapi_in_depth/01_pydantic_models.py
"""
from datetime import date

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator


class Address(BaseModel):
    city: str
    country: str = Field(min_length=2, max_length=2)          # ISO code like "DE"


class UserIn(BaseModel):                                      # what clients SEND
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-z0-9_]+$")
    password: str = Field(min_length=8)
    age: int = Field(ge=13, le=120)                           # 13 <= age <= 120
    birthday: date | None = None                              # "2026-11-08" -> date
    address: Address                                          # nested model
    tags: list[str] = []

    @field_validator("tags")
    @classmethod
    def lowercase_unique(cls, tags: list[str]) -> list[str]:   # clean the value
        return sorted({t.lower() for t in tags})

    @model_validator(mode="after")
    def password_not_username(self) -> "UserIn":               # rules across fields
        if self.username in self.password:
            raise ValueError("password must not contain the username")
        return self


class UserOut(BaseModel):                                     # what we SEND BACK
    username: str
    address: Address                                          # no password here!


# --- 1. Valid input: strings are converted to the right types -------------------------
raw = {"username": "vishal", "password": "s3cret-pass", "age": "30",
       "birthday": "1996-05-04", "address": {"city": "Augsburg", "country": "DE"},
       "tags": ["Python", "python", "Cloud"]}
user = UserIn.model_validate(raw)
print(user.age + 1, type(user.birthday).__name__, user.tags)   # 31 date ['cloud', 'python']

# --- 2. Response models filter out secrets ------------------------------------------------
print(UserOut.model_validate(user.model_dump()).model_dump())
# {'username': 'vishal', 'address': {'city': 'Augsburg', 'country': 'DE'}}

# --- 3. Invalid input: every problem, with where it is -------------------------------------
bad = {"username": "Vi", "password": "vishal123", "age": 7,
       "address": {"city": "Augsburg", "country": "GER"}}
try:
    UserIn.model_validate(bad)
except ValidationError as e:
    for err in e.errors():
        where = ".".join(str(p) for p in err["loc"])
        print(f"  {where:<16} {err['msg']}")

# --- 4. JSON in, JSON out ------------------------------------------------------------------
print(Address.model_validate_json('{"city": "Mumbai", "country": "IN"}').model_dump_json())
