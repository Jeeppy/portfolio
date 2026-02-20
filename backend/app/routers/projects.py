from collections.abc import Sequence

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import true
from sqlmodel import Session, select

from app.database import get_session
from app.models import Project
from app.schemas import ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])
logger = structlog.get_logger()


@router.get("", response_model=list[ProjectRead])
def list_projects(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session),
) -> Sequence[Project]:
    """List published projects.

    Supports pagination via `offset` and `limit` (max 100)."""
    statement = (
        select(Project).where(Project.published == true()).offset(offset).limit(limit)
    )
    return session.exec(statement).all()


@router.get("/{slug}", response_model=ProjectRead)
def get_project(slug: str, session: Session = Depends(get_session)) -> Project:
    """Get a project by its slug.

    Returns 404 if the project does not exist or is not published.
    """
    project = get_project_or_404(slug, session)
    if not project.published:
        logger.warning("Access to unpublished project denied", slug=slug)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project


def get_project_or_404(slug: str, session: Session) -> Project:
    statement = select(Project).where(Project.slug == slug)
    project: Project | None = session.exec(statement).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project
