from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.auth import get_current_admin
from app.database import get_session
from app.models import Project
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectRead])
def list_projects(session: Session = Depends(get_session)) -> Sequence[Project]:
    statement = select(Project).where(Project.published == True)
    return session.exec(statement).all()


@router.get("/{slug}", response_model=ProjectRead)
def get_project(slug: str, session: Session = Depends(get_session)) -> Project:
    return _get_project_or_404(slug, session)


@router.post("", response_model=ProjectRead, status_code=201)
def create_project(
    data: ProjectCreate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> Project:
    try:
        project = Project(**data.model_dump())
        session.add(project)
        session.commit()
        session.refresh(project)
        return project
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(
            status_code=409, detail="Project with this slug already exists."
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
    for key, value in update_data.items():
        setattr(project, key, value)

    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{slug}", status_code=204)
def delete_project(
    slug: str,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin),
) -> None:
    project = _get_project_or_404(slug, session)

    session.delete(project)
    session.commit()


def _get_project_or_404(slug: str, session: Session) -> Project:
    statement = select(Project).where(Project.slug == slug)
    project: Project | None = session.exec(statement).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
