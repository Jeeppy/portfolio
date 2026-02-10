from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Project

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
def list_projects(session: Session = Depends(get_session)) -> Sequence[Project]:
    statement = select(Project).where(Project.published == True)
    return session.exec(statement).all()


@router.get("/{slug}")
def get_project(slug: str, session: Session = Depends(get_session)) -> Project:
    statement = select(Project).where(Project.slug == slug)
    project = session.exec(statement).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("")
def create_project(
    project: Project, session: Session = Depends(get_session)
) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project
