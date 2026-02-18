from collections.abc import Sequence
from datetime import UTC, datetime

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlmodel import Session, select

from app.auth import get_current_admin
from app.database import get_session
from app.limiter import limiter
from app.models import ContactMessage
from app.schemas import ContactCreate, ContactRead

router = APIRouter(prefix="/contact", tags=["contact"])
logger = structlog.get_logger()


def _get_message_or_404(message_id: int, session: Session) -> ContactMessage:
    statement = select(ContactMessage).where(ContactMessage.id == message_id)
    message = session.exec(statement).first()
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    return message


@router.post("", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_message(
    request: Request, data: ContactCreate, session: Session = Depends(get_session)
) -> ContactMessage:
    """Send a contact message.

    Rate-limited to 5 requests per minute per IP.
    """
    message = ContactMessage(**data.model_dump())
    session.add(message)
    session.commit()
    session.refresh(message)

    logger.info("Contact message received", sender=data.email)
    return message


@router.get("", response_model=list[ContactRead])
def list_messages(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Sequence[ContactMessage]:
    """List contact messages (admin only).

    Soft-deleted messages are excluded.
    Supports pagination via `offset` and `limit` (max 100).
    """
    return session.exec(
        select(ContactMessage)
        .where(ContactMessage.deleted_at == None)  # noqa: E711
        .offset(offset)
        .limit(limit)
    ).all()


@router.patch("/{message_id}/read", response_model=ContactRead)
def read_message(
    message_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> ContactMessage:
    """Mark a contact message as read (admin only).

    Returns 404 if the message does not exist.
    """
    message = _get_message_or_404(message_id, session)
    message.read = True

    session.add(message)
    session.commit()
    session.refresh(message)

    logger.info("Message marked as read", message_id=message_id)
    return message


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(
    message_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> None:
    """Soft-delete a contact message (admin only).

    The message is hidden from the list but not removed from the database.
    Returns 404 if the message does not exist.
    """
    message = _get_message_or_404(message_id, session)

    message.deleted_at = datetime.now(UTC)
    session.add(message)
    session.commit()
    logger.info("Message soft-deleted", message_id=message_id)
