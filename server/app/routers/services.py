"""Endpoints for managing services offered by barbers."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from ..dependencies import get_session
from ..models.service import Service
from ..models.user import User
from ..schemas.services import ServiceCreate, ServiceResponse, ServiceUpdate

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=List[ServiceResponse])
async def list_services(
    *,
    session: Session = Depends(get_session),
    barber_id: Optional[UUID] = Query(default=None, description="Filter by barber ID"),
) -> List[ServiceResponse]:
    """Return the catalog of services, optionally filtered by barber."""

    statement = select(Service).order_by(Service.name)
    if barber_id:
        statement = statement.where(Service.barber_id == barber_id)
    services = session.exec(statement).all()
    return [ServiceResponse.model_validate(service) for service in services]


@router.post("", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(
    payload: ServiceCreate,
    session: Session = Depends(get_session),
) -> ServiceResponse:
    """Create a new service for a barber."""

    barber = session.get(User, payload.barber_id)
    if not barber:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Barber not found")

    service = Service(**payload.model_dump())
    session.add(service)
    session.commit()
    session.refresh(service)
    return ServiceResponse.model_validate(service)


@router.patch("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: UUID,
    payload: ServiceUpdate,
    session: Session = Depends(get_session),
) -> ServiceResponse:
    """Update mutable fields on a service record."""

    service = session.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)
    session.add(service)
    session.commit()
    session.refresh(service)
    return ServiceResponse.model_validate(service)


@router.delete("/{service_id}", status_code=status.HTTP_200_OK)
async def delete_service(
    service_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    """Remove a service from the catalog."""

    service = session.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    session.delete(service)
    session.commit()
    return {"detail": "Service deleted"}
