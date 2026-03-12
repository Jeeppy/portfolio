import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.auth import get_current_admin
from app.database import get_session
from app.models import Skill
from app.routers.profile import get_or_create_profile
from app.schemas import SkillCreate, SkillRead, SkillUpdate

router = APIRouter(prefix="/admin/skills", tags=["admin/skills"])
logger = structlog.get_logger()


def get_skill_or_404(id: int, session: Session) -> Skill:
    skill: Skill | None = session.get(Skill, id)
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found"
        )
    return skill


@router.post("", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
def create_skill(
    data: SkillCreate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Skill:
    """Create a new skill (admin only)."""
    try:
        profile_id = get_or_create_profile(session).id
        skill = Skill(**data.model_dump())
        skill.profile_id = profile_id

        session.add(skill)
        session.commit()
        session.refresh(skill)

        logger.info("Skill created", name=skill.name)
        return skill
    except IntegrityError as error:
        session.rollback()
        logger.warning("Duplicate skill name", name=data.name)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Skill already exists"
        ) from error


@router.put("/{id}", response_model=SkillRead)
def update_skill(
    id: int,
    data: SkillUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Skill:
    """Update a skill by its id (admin only).

    Returns 404 if the skill does not exist."""
    skill = get_skill_or_404(id, session)
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(skill, key, value)

    session.add(skill)
    session.commit()
    session.refresh(skill)

    logger.info("Skill updated", id=id)
    return skill


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    id: int,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> None:
    """Delete a skill by its id (admin only).

    Return 404 if the skill does not exist."""
    skill = get_skill_or_404(id, session)

    session.delete(skill)
    session.commit()

    logger.info("Skill deleted", id=id)
