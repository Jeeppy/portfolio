from collections.abc import Sequence

import structlog
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Education
from app.routers.admin.education import get_education_or_404
from app.schemas import EducationRead

router = APIRouter(prefix="/education", tags=["education"])
logger = structlog.get_logger()


@router.get("", response_model=list[EducationRead])
def list_educations(session: Session = Depends(get_session)) -> Sequence[Education]:
    """List all educations."""
    return session.exec(select(Education)).all()


@router.get("/{id}", response_model=EducationRead)
def get_education(
    id: int,
    session: Session = Depends(get_session),
) -> Education:
    """Returns an education by its id.

    Return 404 if the education does not exist."""
    return get_education_or_404(id, session)
