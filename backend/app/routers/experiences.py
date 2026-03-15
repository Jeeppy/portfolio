from collections.abc import Sequence

import structlog
from fastapi import APIRouter, Depends
from sqlmodel import Session, col, select

from app.database import get_session
from app.models import Experience
from app.routers.admin.experiences import get_experience_or_404
from app.schemas import ExperienceRead

router = APIRouter(prefix="/experiences", tags=["experiences"])
logger = structlog.get_logger()


@router.get("", response_model=list[ExperienceRead])
def list_experiences(session: Session = Depends(get_session)) -> Sequence[Experience]:
    """List all experiences."""
    return session.exec(
        select(Experience).order_by(col(Experience.start_date).desc())
    ).all()


@router.get("/{id}", response_model=ExperienceRead)
def get_experience(
    id: int,
    session: Session = Depends(get_session),
) -> Experience:
    """Returns an experience by its id.

    Return 404 if the experience does not exist."""
    return get_experience_or_404(id, session)
