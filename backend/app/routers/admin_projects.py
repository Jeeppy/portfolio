from collections.abc import Sequence
from datetime import UTC, datetime

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.auth import get_current_admin
from app.database import get_session
from app.models import Project, Tag
from app.routers.projects import get_project_or_404
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/admin/projects", tags=["admin/projects"])
logger = structlog.get_logger()


@router.get("", response_model=list[ProjectRead])
def list_all_projects(
    session: Session = Depends(get_session), _: str = Depends(get_current_admin)
) -> Sequence[Project]:
    """List all project including unpublished drafts (admin only)."""
    return session.exec(select(Project)).all()


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Project:
    """Create a new project (admin only).

    Returns 409 if a project with the same slug already exists.
    Tags are created automatically if they do not exist yet.
    """
    try:
        project = Project(**data.model_dump(exclude={"tags"}))
        session.add(project)

        for tag_name in data.tags:
            tag: Tag | None = session.exec(
                select(Tag).where(Tag.name == tag_name)
            ).first()
            if tag is None:
                tag = Tag(name=tag_name)
            project.tags.append(tag)
        session.commit()
        session.refresh(project)

        logger.info("Project created", slug=project.slug)
        return project

    except IntegrityError as error:
        session.rollback()
        logger.warning("Duplicate project slug", slug=data.slug)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project with this slug already exists.",
        ) from error


@router.put("/{slug}", response_model=ProjectRead)
def update_project(
    slug: str,
    data: ProjectUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Project:
    """Update a project by its slug (admin only).

    Only provided fields are updated. Providing `tags` fully replaces the existing tag list;
    pass an empty list to remove all tags.
    Returns 404 if the project does not exist."""
    project = get_project_or_404(slug, session)

    update_data = data.model_dump(exclude_unset=True)
    tag_names = update_data.pop("tags", None)

    for key, value in update_data.items():
        setattr(project, key, value)

    if tag_names is not None:
        project.tags.clear()
        for tag_name in tag_names:
            tag: Tag | None = session.exec(
                select(Tag).where(Tag.name == tag_name)
            ).first()
            if tag is None:
                tag = Tag(name=tag_name)
            project.tags.append(tag)
    project.updated_at = datetime.now(UTC)

    session.add(project)
    session.commit()
    session.refresh(project)

    logger.info("Project updated", slug=slug)
    return project


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    slug: str,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> None:
    """Delete a project by its slug (admin only).

    Returns 404 if the project does not exist."""
    project = get_project_or_404(slug, session)

    session.delete(project)
    session.commit()
    logger.info("Project deleted", slug=slug)
