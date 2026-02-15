from collections.abc import Sequence
from datetime import UTC, datetime

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import true
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.auth import get_current_admin, get_optional_admin
from app.database import get_session
from app.models import Project, Tag
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])
logger = structlog.get_logger()


@router.get("", response_model=list[ProjectRead])
def list_projects(
    all: bool = False,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session),
    admin: str | None = Depends(get_optional_admin),
) -> Sequence[Project]:
    if all and admin:
        return session.exec(select(Project)).all()
    statement = (
        select(Project).where(Project.published == true()).offset(offset).limit(limit)
    )
    return session.exec(statement).all()


@router.get("/{slug}", response_model=ProjectRead)
def get_project(slug: str, session: Session = Depends(get_session)) -> Project:
    project = _get_project_or_404(slug, session)
    if not project.published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Project:
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
    project = _get_project_or_404(slug, session)

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
    project = _get_project_or_404(slug, session)

    session.delete(project)
    session.commit()
    logger.info("Project deleted", slug=slug)


def _get_project_or_404(slug: str, session: Session) -> Project:
    statement = select(Project).where(Project.slug == slug)
    project: Project | None = session.exec(statement).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project
