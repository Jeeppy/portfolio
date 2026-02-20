import structlog
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Profile
from app.schemas import ProfileRead

router = APIRouter(prefix="/profile", tags=["profile"])
logger = structlog.get_logger()


@router.get("", response_model=ProfileRead)
def get_profile(session: Session = Depends(get_session)) -> Profile:
    """Get the portfolio profile.

    Creates and returns an empty profile if none exists yet.
    """
    return get_or_create_profile(session)


def get_or_create_profile(session: Session) -> Profile:
    profile: Profile | None = session.exec(select(Profile)).first()
    if profile is None:
        profile = Profile()
        session.add(profile)
        session.commit()
        session.refresh(profile)
        logger.info("Profile created", profile_id=profile.id)
    return profile
