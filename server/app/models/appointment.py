"""SQLModel mapping for a booked appointment."""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Appointment(SQLModel, table=True):
    """A concrete booking between a customer and a barber."""

    __tablename__ = "appointments"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    barber_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    customer_name: str
    customer_contact: Optional[str] = None
    start_time: datetime = Field(index=True)
    duration_minutes: int = Field(gt=0, lt=8 * 60)
    notes: Optional[str] = None
    service_id: Optional[UUID] = Field(default=None, foreign_key="services.id")

    # Relationships can be added later if eager loading is required.
