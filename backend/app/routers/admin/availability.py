import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.auth import get_current_admin
from app.database import get_session
from app.models import AvailabilitySlot
from app.schemas import AvailabilitySlotCreate, AvailabilitySlotRead

router = APIRouter(prefix="/admin/availability", tags=["admin/availability"])
logger = structlog.get_logger()


@router.get("", response_model=list[AvailabilitySlotRead])
def list_slots(
    session: Session = Depends(get_session), _: str = Depends(get_current_admin)
) -> list[AvailabilitySlot]:
    """List all availability slots (admin only)."""
    return list(session.exec(select(AvailabilitySlot)).all())


@router.post(
    "", response_model=AvailabilitySlotRead, status_code=status.HTTP_201_CREATED
)
def create_slot(
    data: AvailabilitySlotCreate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> AvailabilitySlot:
    """Create an availability slot (admin only)."""
    slot = AvailabilitySlot(**data.model_dump())
    session.add(slot)
    session.commit()
    session.refresh(slot)
    logger.info("Availability slot created", slot_id=slot.id)
    return slot


@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(
    slot_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> None:
    """Delete an availability slot (admin only)."""
    slot = session.get(AvailabilitySlot, slot_id)
    if slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found"
        )
    session.delete(slot)
    session.commit()
    logger.info("Availability slot deleted", slot_id=slot.id)
