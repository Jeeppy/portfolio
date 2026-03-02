from collections.abc import Sequence

import structlog
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Skill
from app.schemas import SkillRead

router = APIRouter(prefix="/skills", tags=["skills"])
logger = structlog.get_logger()


@router.get("", response_model=list[SkillRead])
def list_skills(session: Session = Depends(get_session)) -> Sequence[Skill]:
    """List all skills."""
    return session.exec(select(Skill)).all()
