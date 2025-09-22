"""Utilities for seeding the database with demo data."""
from __future__ import annotations

from datetime import datetime, time, timedelta, timezone

from sqlmodel import Session, select

from .models.appointment import Appointment
from .models.service import Service
from .models.user import User
from .models.working_hour import WorkingHour
from .utils.security import hash_password


def seed_demo_data(engine) -> None:
    """Populate the database with a barber, services, hours, and appointments."""

    with Session(engine) as session:
        has_users = session.exec(select(User).limit(1)).first()
        if has_users:
            return

        barber = User(
            email="barber@example.com",
            full_name="Jordan Styles",
            password_hash=hash_password("password123"),
            role="barber",
        )
        session.add(barber)
        session.commit()
        session.refresh(barber)

        services = [
            Service(
                barber_id=barber.id,
                name="Signature Fade",
                description="Detailed fade with line up and style",
                duration_minutes=45,
                price=30.0,
            ),
            Service(
                barber_id=barber.id,
                name="Beard Trim",
                description="Beard sculpting with hot towel finish",
                duration_minutes=30,
                price=18.0,
            ),
        ]
        session.add_all(services)
        session.commit()
        for service in services:
            session.refresh(service)

        working_hours = [
            WorkingHour(
                barber_id=barber.id,
                day_of_week=day,
                start_time=time(9, 0),
                end_time=time(17, 0),
            )
            for day in range(0, 5)
        ]
        session.add_all(working_hours)

        base = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        appointments = [
            Appointment(
                barber_id=barber.id,
                customer_name="Alex Fade",
                customer_contact="alex@example.com",
                start_time=base + timedelta(days=1, hours=2),
                duration_minutes=45,
                notes="First-time visitor, prefers clippers.",
                service_id=services[0].id,
            ),
            Appointment(
                barber_id=barber.id,
                customer_name="Maria Line",
                customer_contact="+30 555 1234",
                start_time=base + timedelta(days=2, hours=1, minutes=30),
                duration_minutes=30,
                notes="Add beard balm.",
                service_id=services[1].id,
            ),
        ]
        session.add_all(appointments)
        session.commit()
