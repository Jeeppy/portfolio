import structlog
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth import get_current_admin
from app.database import get_session
from app.models import Education, Experience, Profile, Skill
from app.routers.profile import get_or_create_profile
from app.schemas import ProfileRead, ProfileUpdate

router = APIRouter(prefix="/admin/profile", tags=["admin/profile"])
logger = structlog.get_logger()


@router.put("", response_model=ProfileRead)
def update_profile(
    data: ProfileUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Profile:
    """Update the portfolio profile (admin only).

    Only provided fields are updated. Nested collections (skills, experiences, education) fully replace
    the existing list when included.
    """
    profile = get_or_create_profile(session)

    update_data = data.model_dump(exclude_unset=True)
    skills_data = update_data.pop("skills", None)
    experiences_data = update_data.pop("experiences", None)
    education_data = update_data.pop("education", None)

    for key, value in update_data.items():
        setattr(profile, key, value)

    if skills_data is not None:
        profile.skills = [Skill(**s, profile_id=profile.id) for s in skills_data]

    if experiences_data is not None:
        profile.experiences = [
            Experience(**e, profile_id=profile.id) for e in experiences_data
        ]

    if education_data is not None:
        profile.education = [
            Education(**e, profile_id=profile.id) for e in education_data
        ]

    session.add(profile)
    session.commit()
    session.refresh(profile)

    logger.info("Profile updated", profile_id=profile.id)
    return profile
