"""Authentication related API routes backed by the database."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..dependencies import get_session
from ..models.user import User
from ..schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserPublic
from ..utils.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: RegisterRequest,
    session: Session = Depends(get_session),
) -> AuthResponse:
    """Register a new staff account if the email is not already taken."""

    email = payload.email.lower()
    existing = session.exec(select(User).where(User.email == email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    user = User(email=email, full_name=payload.full_name, password_hash=hash_password(payload.password))
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token(subject=str(user.id))
    return AuthResponse(
        message="Registration successful",
        user=UserPublic.model_validate(user),
        access_token=token,
    )


@router.post("/login", response_model=AuthResponse)
async def login_user(
    payload: LoginRequest,
    session: Session = Depends(get_session),
) -> AuthResponse:
    """Authenticate an existing staff member and issue an access token."""

    email = payload.email.lower()
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(subject=str(user.id))
    return AuthResponse(message="Login successful", user=UserPublic.model_validate(user), access_token=token)
