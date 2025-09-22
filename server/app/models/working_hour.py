"""SQLModel representation of a barber's weekly schedule."""
from __future__ import annotations

from datetime import time
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class WorkingHour(SQLModel, table=True):
    """Defines when a barber is available for bookings."""

    __tablename__ = "working_hours"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    barber_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    day_of_week: int = Field(ge=0, le=6, nullable=False)
    start_time: time
    end_time: time

    # Relationship backrefs can be introduced later as the domain grows.
