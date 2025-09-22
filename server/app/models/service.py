"""SQLModel representation of services offered by a barber."""
from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Service(SQLModel, table=True):
    """Services that can be booked during an appointment."""

    __tablename__ = "services"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    barber_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    duration_minutes: int = Field(gt=0)
    price: float = Field(gt=0)

    # Relationship fields omitted for now; lookups can be performed via joins.
