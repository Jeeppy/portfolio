import structlog
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlmodel import Session

import app.uploads as file_uploads
from app.auth import get_current_admin
from app.database import get_session
from app.models import Education, Experience, Profile, Skill, SocialLink
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
    social_links_data = update_data.pop("social_links", None)

    for key, value in update_data.items():
        setattr(profile, key, value)

    if skills_data is not None:
        profile.skills = [Skill(**s, profile_id=profile.id) for s in skills_data]

    if experiences_data is not None:
        profile.experiences = [
            Experience(**e, profile_id=profile.id) for e in experiences_data
        ]

    if education_data is not None:
        education_list = []
        for e in education_data:
            exp_id = e.get("experience_id")
            if exp_id is not None:
                exp = session.get(Experience, exp_id)
                if exp is None or exp.profile_id != profile.id:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                        detail=f"Experience {exp_id} not found or does not belong to this profile",
                    )
            education_list.append(Education(**e, profile_id=profile.id))
        profile.education = education_list

    if social_links_data is not None:
        profile.social_links = [
            SocialLink(**sl, profile_id=profile.id) for sl in social_links_data
        ]

    session.add(profile)
    session.commit()
    session.refresh(profile)

    logger.info("Profile updated", profile_id=profile.id)
    return profile


@router.post("/avatar", response_model=ProfileRead)
async def upload_avatar(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Profile:
    """Upload or replace the profile avatar (admin only)."""
    profile = get_or_create_profile(session)
    if profile.avatar_filename:
        file_uploads.delete_file(file_uploads.AVATAR_DIR, profile.avatar_filename)
    filename = await file_uploads.save_upload(
        file,
        file_uploads.AVATAR_DIR,
        file_uploads.ALLOWED_AVATAR_TYPES,
        file_uploads.AVATAR_MAX_SIZE,
    )
    profile.avatar_filename = filename
    session.add(profile)
    session.commit()
    session.refresh(profile)
    logger.info("Avatar uploaded", profile_id=profile.id, filename=filename)
    return profile


@router.delete("/avatar", response_model=ProfileRead)
def delete_avatar(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Profile:
    """Delete the profile avatar (admin only)."""
    profile = get_or_create_profile(session)
    if profile.avatar_filename:
        file_uploads.delete_file(file_uploads.AVATAR_DIR, profile.avatar_filename)
        profile.avatar_filename = None
        session.add(profile)
        session.commit()
        session.refresh(profile)
        logger.info("Avatar deleted", profile_id=profile.id)
    return profile


@router.post("/resume", response_model=ProfileRead)
async def upload_resume(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Profile:
    """Upload or replace the profile resume (admin only)."""
    profile = get_or_create_profile(session)
    if profile.resume_filename:
        file_uploads.delete_file(file_uploads.RESUME_DIR, profile.resume_filename)
    filename = await file_uploads.save_upload(
        file,
        file_uploads.RESUME_DIR,
        file_uploads.ALLOWED_RESUME_TYPES,
        file_uploads.RESUME_MAX_SIZE,
    )
    profile.resume_filename = filename
    session.add(profile)
    session.commit()
    session.refresh(profile)
    logger.info("Resume uploaded", profile_id=profile.id, filename=filename)
    return profile


@router.delete("/resume", response_model=ProfileRead)
def delete_resume(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Profile:
    """Delete the profile resume (admin only)."""
    profile = get_or_create_profile(session)
    if profile.resume_filename:
        file_uploads.delete_file(file_uploads.RESUME_DIR, profile.resume_filename)
        profile.resume_filename = None
        session.add(profile)
        session.commit()
        session.refresh(profile)
        logger.info("Resume deleted", profile_id=profile.id)
    return profile
