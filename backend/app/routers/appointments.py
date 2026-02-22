from datetime import date

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import true
from sqlmodel import Session, select

from app.database import get_session
from app.limiter import limiter
from app.models import Appointment, AvailabilitySlot
from app.schemas import AppointmentCreate, AppointmentRead, AvailabilitySlotRead

router = APIRouter(prefix="/appointments", tags=["appointments"])
logger = structlog.get_logger()


@router.get("/available", response_model=list[AvailabilitySlotRead])
def get_available_slots(
    appointment_date: date, session: Session = Depends(get_session)
) -> list[AvailabilitySlot]:
    """Returns active slots for a given date, excluding already booked ones."""
    day_of_week = appointment_date.weekday()

    active_slots = session.exec(
        select(AvailabilitySlot).where(
            AvailabilitySlot.day_of_week == day_of_week,
            AvailabilitySlot.is_active == true(),
        )
    ).all()

    booked = session.exec(
        select(Appointment).where(
            Appointment.appointment_date == appointment_date,
            Appointment.status != "declined",
            Appointment.status != "cancelled",
        )
    )

    booked_times = {appointment.start_time for appointment in booked}

    return [s for s in active_slots if s.start_time not in booked_times]


@router.post("", response_model=AppointmentRead, status_code=201)
@limiter.limit("5/hour")
def create_appointment(
    request: Request,
    data: AppointmentCreate,
    session: Session = Depends(get_session),
) -> Appointment:
    if data.appointment_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Appointment date mist be in the future",
        )

    already_booked = session.exec(
        select(Appointment).where(
            Appointment.appointment_date == data.appointment_date,
            Appointment.start_time == data.start_time,
            Appointment.status != "declined",
        )
    ).first()

    if already_booked:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This slot is already booked",
        )

    appointment = Appointment(**data.model_dump())
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    logger.info("Appointment created", appointment_id=appointment.id)
    return appointment
