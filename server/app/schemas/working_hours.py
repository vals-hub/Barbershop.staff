"""Schemas for working hour management."""
from __future__ import annotations
from datetime import time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, conint, model_validator


class WorkingHourBase(BaseModel):
    """Shared attributes for creating or updating working hours."""

    barber_id: UUID
    day_of_week: conint(ge=0, le=6)  # type: ignore[valid-type]
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def validate_window(self) -> "WorkingHourBase":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class WorkingHourCreate(WorkingHourBase):
    """Payload for creating a new availability window."""

    pass


class WorkingHourUpdate(BaseModel):
    """Fields that can be updated on an existing working hour record."""

    start_time: Optional[time] = None
    end_time: Optional[time] = None

    @model_validator(mode="after")
    def validate_window(self) -> "WorkingHourUpdate":
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class WorkingHourResponse(BaseModel):
    """Serialized representation of a barber availability window."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    barber_id: UUID
    day_of_week: int
    start_time: time
    end_time: time
