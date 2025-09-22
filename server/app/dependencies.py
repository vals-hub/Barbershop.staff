"""Common dependency providers for FastAPI routers."""
from __future__ import annotations

from sqlmodel import Session

from .database import get_session

__all__ = ["get_session", "Session"]
