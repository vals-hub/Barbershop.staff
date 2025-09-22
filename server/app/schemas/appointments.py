"""Schemas for appointment endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, conint


class AppointmentCreate(BaseModel):
    """Payload required to create or update an appointment."""

    barber_id: UUID
    customer_name: str = Field(..., min_length=1, max_length=100)
    customer_contact: Optional[str] = Field(default=None, max_length=100)
    service_id: Optional[UUID] = None
    start_time: datetime
    duration_minutes: conint(gt=0, le=8 * 60)  # type: ignore[valid-type]
    notes: Optional[str] = Field(default=None, max_length=255)


class AppointmentResponse(BaseModel):
    """Appointment object returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    barber_id: UUID
    customer_name: str
    customer_contact: Optional[str] = None
    service_id: Optional[UUID] = None
    start_time: datetime
    duration_minutes: int
    notes: Optional[str] = None
