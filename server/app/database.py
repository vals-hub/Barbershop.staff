"""Database configuration and lifecycle helpers."""
from __future__ import annotations

from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine

from .config import settings
from . import models  # ensure models are imported for SQLModel metadata

_connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, echo=False, connect_args=_connect_args)


def init_db() -> None:
    """Create database tables and seed demo data when empty."""

    SQLModel.metadata.create_all(engine)
    from .seed import seed_demo_data

    seed_demo_data(engine)


def get_session() -> Iterator[Session]:
    """Yield a SQLModel session for request handling."""

    with Session(engine) as session:
        yield session
