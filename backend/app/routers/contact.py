from collections.abc import Sequence

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.auth import get_current_admin
from app.database import get_session
from app.models import ContactMessage
from app.schemas import ContactCreate, ContactRead

router = APIRouter(prefix="/contact", tags=["contact"])
logger = structlog.get_logger()


@router.post("", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
def create_message(
    data: ContactCreate, session: Session = Depends(get_session)
) -> ContactMessage:
    message = ContactMessage(**data.model_dump())
    session.add(message)
    session.commit()
    session.refresh(message)

    logger.info("Contact message received", sender=data.email)
    return message


@router.get("", response_model=list[ContactRead])
def list_messages(
    session: Session = Depends(get_session), _: str = Depends(get_current_admin)
) -> Sequence[ContactMessage]:
    return session.exec(select(ContactMessage)).all()


@router.patch("/{message_id}/read", response_model=ContactRead)
def read_message(
    message_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> ContactMessage:
    statement = select(ContactMessage).where(ContactMessage.id == message_id)
    message: ContactMessage | None = session.exec(statement).first()
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )

    message.read = True
    session.add(message)
    session.commit()
    session.refresh(message)

    logger.info("Message marked as read", message_id=message_id)
    return message
