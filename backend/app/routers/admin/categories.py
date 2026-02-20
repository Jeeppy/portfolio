from collections.abc import Sequence

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.auth import get_current_admin
from app.database import get_session
from app.models import ProjectCategory
from app.schemas import ProjectCategoryCreate, ProjectCategoryRead

router = APIRouter(prefix="/admin/categories", tags=["admin/categories"])
logger = structlog.get_logger()


def get_category_or_404(slug: str, session: Session) -> ProjectCategory:
    category: ProjectCategory | None = session.exec(
        select(ProjectCategory).where(ProjectCategory.slug == slug)
    ).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@router.get("", response_model=list[ProjectCategoryRead])
def list_categories(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Sequence[ProjectCategory]:
    """List all project categories (admin only)."""
    return session.exec(select(ProjectCategory)).all()


@router.post(
    "", response_model=ProjectCategoryRead, status_code=status.HTTP_201_CREATED
)
def create_category(
    data: ProjectCategoryCreate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> ProjectCategory:
    """Create a new project category (admin only).

    Return 409 if a category with the same name or slug already exists.
    """
    try:
        category = ProjectCategory(**data.model_dump())
        session.add(category)
        session.commit()
        session.refresh(category)
        logger.info("Category created", slug=category.slug)
        return category
    except IntegrityError as error:
        session.rollback()
        logger.warning("Duplicate category", slug=data.slug)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name or slug already exists.",
        ) from error


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    slug: str,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> None:
    """Delete a project category (admin only).

    Returns 404 if the category does not exist.
    """
    category = get_category_or_404(slug, session)
    session.delete(category)
    session.commit()
    logger.info("Category deleted", slug=slug)
