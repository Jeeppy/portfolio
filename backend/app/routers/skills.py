from collections.abc import Sequence

import structlog
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Skill
from app.routers.admin.skills import get_skill_or_404
from app.schemas import SkillRead

router = APIRouter(prefix="/skills", tags=["skills"])
logger = structlog.get_logger()


@router.get("", response_model=list[SkillRead])
def list_skills(session: Session = Depends(get_session)) -> Sequence[Skill]:
    """List all skills."""
    return session.exec(select(Skill)).all()


@router.get("/{id}", response_model=SkillRead)
def get_skill(
    id: int,
    session: Session = Depends(get_session),
) -> Skill:
    """Returns a skill by it id.

    Return 404 if  the skill does not exists."""
    return get_skill_or_404(id, session)
