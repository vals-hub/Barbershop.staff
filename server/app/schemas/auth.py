"""Request and response models for authentication routes."""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    """Payload required to create a new user."""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """Payload used during user authentication."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserPublic(BaseModel):
    """Public representation of a user returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str
    role: str


class AuthResponse(BaseModel):
    """Standard response returned after registration or login."""

    message: str
    user: UserPublic
    access_token: Optional[str] = None
    token_type: str = "bearer"
