"""Database engine and the session-per-request dependency (Module 23)."""
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from taskboard.config import settings


class Base(DeclarativeBase):
    pass


def make_engine(url: str):  # type: ignore[no-untyped-def]
    if url.startswith("sqlite"):
        extra = {"poolclass": StaticPool} if url in ("sqlite://", "sqlite:///:memory:") else {}
        return create_engine(url, connect_args={"check_same_thread": False}, **extra)
    return create_engine(url, pool_pre_ping=True)     # Postgres / Azure SQL in production


engine = make_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
