"""SQLModel representation of a barber/staff user."""
from __future__ import annotations

from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Persisted staff member that can manage the barbershop schedule."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(index=True, unique=True, nullable=False)
    full_name: str
    password_hash: str
    role: str = Field(default="barber")
    is_active: bool = Field(default=True)

    # Relationship fields intentionally omitted for simplicity; queries can join
    # on foreign keys as needed without eager loading.
