import structlog
from fastapi import APIRouter, Depends, Request, status
from sqlmodel import Session

from app.database import get_session
from app.limiter import limiter
from app.models import ContactMessage
from app.schemas import ContactCreate, ContactRead

router = APIRouter(prefix="/contact", tags=["contact"])
logger = structlog.get_logger()


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
