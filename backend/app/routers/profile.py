import structlog
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.auth import get_current_admin
from app.database import get_session
from app.models import Education, Experience, Profile, Skill
from app.schemas import ProfileRead, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])
logger = structlog.get_logger()


@router.get("", response_model=ProfileRead)
def get_profile(session: Session = Depends(get_session)) -> Profile:
    return _get_or_create_profile(session)


@router.put("", response_model=ProfileRead)
def update_profile(
    data: ProfileUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Profile:
    profile = _get_or_create_profile(session)

    update_data = data.model_dump(exclude_unset=True)
    skills_data = update_data.pop("skills", None)
    experiences_data = update_data.pop("experiences", None)
    education_data = update_data.pop("education", None)

    for key, value in update_data.items():
        setattr(profile, key, value)

    if skills_data is not None:
        for skill in profile.skills:
            session.delete(skill)
        profile.skills = [Skill(**s, profile_id=profile.id) for s in skills_data]

    if experiences_data is not None:
        for exp in profile.experiences:
            session.delete(exp)
        profile.experiences = [
            Experience(**e, profile_id=profile.id) for e in experiences_data
        ]

    if education_data is not None:
        for edu in profile.education:
            session.delete(edu)
        profile.education = [
            Education(**e, profile_id=profile.id) for e in education_data
        ]

    session.add(profile)
    session.commit()
    session.refresh(profile)

    logger.info("Profile updated")
    return profile


def _get_or_create_profile(session: Session) -> Profile:
    profile: Profile | None = session.exec(select(Profile)).first()
    if profile is None:
        profile = Profile()
        session.add(profile)
        session.commit()
        session.refresh(profile)
        logger.info("Profile created")
    return profile
