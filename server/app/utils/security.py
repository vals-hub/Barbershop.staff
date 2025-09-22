"""Security helpers for hashing passwords and issuing JWT access tokens."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from ..config import settings

# Bcrypt remains the go-to for password hashing in Python applications and the
# ``passlib`` context takes care of sensible defaults and future migrations.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return a salted hash for ``password`` suitable for persistent storage."""

    return pwd_context.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify that ``password`` matches ``stored_hash`` from the database."""

    return pwd_context.verify(password, stored_hash)


def create_access_token(*, subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Issue a signed JWT for ``subject`` with an optional expiration window."""

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)
