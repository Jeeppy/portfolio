import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.auth import get_current_admin
from app.database import get_session
from app.models import Education
from app.routers.profile import get_or_create_profile
from app.schemas import EducationCreate, EducationRead, EducationUpdate

router = APIRouter(prefix="/admin/education", tags=["admin/education"])
logger = structlog.get_logger()


def get_education_or_404(id: int, session: Session) -> Education:
    education: Education | None = session.get(Education, id)
    if education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Education not found"
        )
    return education


@router.post("", response_model=EducationRead, status_code=status.HTTP_201_CREATED)
def create_education(
    data: EducationCreate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Education:
    """Create a new education (admin only)."""
    profile_id = get_or_create_profile(session).id
    education = Education(**data.model_dump())
    education.profile_id = profile_id

    session.add(education)
    session.commit()
    session.refresh(education)

    logger.info("Education created", name=education.school)
    return education


@router.put("/{id}", response_model=EducationRead)
def update_education(
    id: int,
    data: EducationUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Education:
    """Update an education by its id (admin only).

    Returns 404 if the education does not exist."""
    education = get_education_or_404(id, session)
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(education, key, value)

    session.add(education)
    session.commit()
    session.refresh(education)

    logger.info("Education updated", id=id)
    return education


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(
    id: int,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> None:
    """Delete an education by its id (admin only).

    Return 404 if the education does not exist."""
    education = get_education_or_404(id, session)

    session.delete(education)
    session.commit()

    logger.info("Education deleted", id=id)
