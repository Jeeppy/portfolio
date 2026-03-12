import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.auth import get_current_admin
from app.database import get_session
from app.models import Appointment
from app.schemas import AppointmentRead, AppointmentStatusUpdate

router = APIRouter(prefix="/admin/appointments", tags=["admin/appointments"])
logger = structlog.get_logger()

VALID_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"confirmed", "declined"},
    "confirmed": {"cancelled"},
    "declined": set(),
    "cancelled": set(),
}


@router.get("", response_model=list[AppointmentRead])
def list_appointments(
    status_filter: str | None = None,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> list[Appointment]:
    """List all appointments, optionnally filtered by status."""
    query = select(Appointment)
    if status_filter:
        query = query.where(Appointment.status == status_filter)
    return list(session.exec(query).all())


@router.patch("/{appointment_id}/status", response_model=AppointmentRead)
def update_appointment_status(
    appointment_id: int,
    data: AppointmentStatusUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Appointment:
    """Update the status of an appointment (admin only)."""
    appointment = _get_appointment_or_404(appointment_id, session)

    allowed = VALID_TRANSITIONS.get(appointment.status, set())
    if data.status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Cannot transition from '{appointment.status}' to '{data.status}'",
        )

    appointment.status = data.status
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    logger.info(
        "Appointment status updated", appointment_id=appointment.id, status=data.status
    )
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
    appointment_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> None:
    """Delete an appointment (admin only)."""
    appointment = _get_appointment_or_404(appointment_id, session)
    session.delete(appointment)
    session.commit()
    logger.info("Appointment deleted", appointment_id=appointment.id)


def _get_appointment_or_404(appointment_id: int, session: Session) -> Appointment:
    appointment = session.get(Appointment, appointment_id)
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )
    return appointment
