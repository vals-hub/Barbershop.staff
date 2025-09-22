"""Routes that expose appointment information backed by SQLModel."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from ..dependencies import get_session
from ..models.appointment import Appointment
from ..models.service import Service
from ..models.user import User
from ..schemas.appointments import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["appointments"])


# FastAPI will coerce SQLModel instances into the configured response model, but
# explicitly mapping keeps the handler return annotations accurate and future
# changes safer.
@router.get("", response_model=List[AppointmentResponse])
async def list_appointments(
    *,
    session: Session = Depends(get_session),
    barber_id: Optional[UUID] = Query(default=None, description="Filter by barber ID"),
) -> List[AppointmentResponse]:
    """Return appointments optionally filtered by barber."""

    statement = select(Appointment).order_by(Appointment.start_time)
    if barber_id:
        statement = statement.where(Appointment.barber_id == barber_id)

    appointments = session.exec(statement).all()
    return [AppointmentResponse.model_validate(appointment) for appointment in appointments]


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    payload: AppointmentCreate,
    session: Session = Depends(get_session),
) -> AppointmentResponse:
    """Create a new appointment in the database."""

    barber = session.get(User, payload.barber_id)
    if not barber:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Barber not found")

    if payload.service_id:
        service = session.get(Service, payload.service_id)
        if not service or service.barber_id != payload.barber_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service is not available for the selected barber",
            )

    appointment = Appointment(**payload.model_dump())
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    return AppointmentResponse.model_validate(appointment)
