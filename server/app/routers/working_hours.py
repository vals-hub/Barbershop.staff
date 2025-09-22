"""Endpoints for managing barber availability windows."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from ..dependencies import get_session
from ..models.user import User
from ..models.working_hour import WorkingHour
from ..schemas.working_hours import WorkingHourCreate, WorkingHourResponse, WorkingHourUpdate

router = APIRouter(prefix="/working-hours", tags=["working-hours"])


@router.get("", response_model=List[WorkingHourResponse])
async def list_working_hours(
    *,
    session: Session = Depends(get_session),
    barber_id: Optional[UUID] = Query(default=None, description="Filter by barber ID"),
) -> List[WorkingHourResponse]:
    """Return configured working hours, optionally filtered by barber."""

    statement = select(WorkingHour).order_by(
        WorkingHour.barber_id, WorkingHour.day_of_week, WorkingHour.start_time
    )
    if barber_id:
        statement = statement.where(WorkingHour.barber_id == barber_id)
    hours = session.exec(statement).all()
    return [WorkingHourResponse.model_validate(hour) for hour in hours]


@router.post("", response_model=WorkingHourResponse, status_code=status.HTTP_201_CREATED)
async def create_working_hour(
    payload: WorkingHourCreate,
    session: Session = Depends(get_session),
) -> WorkingHourResponse:
    """Create a new availability window for a barber."""

    barber = session.get(User, payload.barber_id)
    if not barber:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Barber not found")

    existing = session.exec(
        select(WorkingHour).where(
            WorkingHour.barber_id == payload.barber_id,
            WorkingHour.day_of_week == payload.day_of_week,
        )
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Working hours already defined for this day. Update the existing entry instead.",
        )

    working_hour = WorkingHour(**payload.model_dump())
    session.add(working_hour)
    session.commit()
    session.refresh(working_hour)
    return WorkingHourResponse.model_validate(working_hour)


@router.patch("/{working_hour_id}", response_model=WorkingHourResponse)
async def update_working_hour(
    working_hour_id: UUID,
    payload: WorkingHourUpdate,
    session: Session = Depends(get_session),
) -> WorkingHourResponse:
    """Update the start/end times for a working hour entry."""

    working_hour = session.get(WorkingHour, working_hour_id)
    if not working_hour:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Working hour not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(working_hour, field, value)
    session.add(working_hour)
    session.commit()
    session.refresh(working_hour)
    return WorkingHourResponse.model_validate(working_hour)


@router.delete("/{working_hour_id}", status_code=status.HTTP_200_OK)
async def delete_working_hour(
    working_hour_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    """Delete a working hour entry."""

    working_hour = session.get(WorkingHour, working_hour_id)
    if not working_hour:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Working hour not found")

    session.delete(working_hour)
    session.commit()
    return {"detail": "Working hour deleted"}
