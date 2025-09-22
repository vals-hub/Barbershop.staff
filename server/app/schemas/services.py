"""Schemas for service management endpoints."""
from __future__ import annotations
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, confloat, conint


class ServiceCreate(BaseModel):
    """Fields required to create a new service offering."""

    barber_id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    duration_minutes: conint(gt=0, le=8 * 60)  # type: ignore[valid-type]
    price: confloat(gt=0)  # type: ignore[valid-type]


class ServiceUpdate(BaseModel):
    """Mutable fields for updating an existing service."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    duration_minutes: Optional[conint(gt=0, le=8 * 60)] = None  # type: ignore[valid-type]
    price: Optional[confloat(gt=0)] = None  # type: ignore[valid-type]


class ServiceResponse(BaseModel):
    """Serialized representation of a service."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    barber_id: UUID
    name: str
    description: Optional[str] = None
    duration_minutes: int
    price: float
