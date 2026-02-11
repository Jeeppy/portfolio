from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.auth import get_current_admin
from app.database import get_session
from app.models import Profile
from app.schemas import ProfileRead, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])


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
    for key, value in update_data.items():
        setattr(profile, key, value)

    session.add(profile)
    session.commit()
    session.refresh(profile)

    return profile


def _get_or_create_profile(session: Session) -> Profile:
    profile: Profile | None = session.exec(select(Profile)).first()
    if profile is None:
        profile = Profile()
        session.add(profile)
        session.commit()
        session.refresh(profile)
    return profile
