import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.auth import get_current_admin
from app.database import get_session
from app.models import Experience
from app.routers.profile import get_or_create_profile
from app.schemas import ExperienceCreate, ExperienceRead, ExperienceUpdate

router = APIRouter(prefix="/admin/experiences", tags=["admin/experiences"])
logger = structlog.get_logger()


def get_experience_or_404(id: int, session: Session) -> Experience:
    experience: Experience | None = session.get(Experience, id)
    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found"
        )
    return experience


@router.post("", response_model=ExperienceRead, status_code=status.HTTP_201_CREATED)
def create_experience(
    data: ExperienceCreate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Experience:
    """Create a new experience (admin only)."""
    profile_id = get_or_create_profile(session).id
    experience = Experience(**data.model_dump())
    experience.profile_id = profile_id

    session.add(experience)
    session.commit()
    session.refresh(experience)

    logger.info("Experience created", name=experience.company)
    return experience


@router.put("/{id}", response_model=ExperienceRead)
def update_experience(
    id: int,
    data: ExperienceUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Experience:
    """Update an experience by its id (admin only).

    Returns 404 if the experience does not exist."""
    experience = get_experience_or_404(id, session)
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(experience, key, value)

    session.add(experience)
    session.commit()
    session.refresh(experience)

    logger.info("Experience updated", id=id)
    return experience


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experience(
    id: int,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> None:
    """Delete an experience by its id (admin only).

    Return 404 if the experience does not exist."""
    experience = get_experience_or_404(id, session)

    session.delete(experience)
    session.commit()

    logger.info("Experience deleted", id=id)
