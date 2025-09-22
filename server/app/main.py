"""Entry point for the FastAPI application."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings
from .database import init_db
from .routers import appointments, auth, services, working_hours


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables and seed demo content on startup."""

    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)


@app.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    """Return a basic application health payload."""

    return {"status": "ok", "environment": settings.environment}


# Register routers under the `/api` prefix so paths match Render expectations.
app.include_router(auth.router, prefix="/api")
app.include_router(appointments.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(working_hours.router, prefix="/api")
