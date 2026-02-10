from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/projects", tags=["projects"])

PROJECTS = [
    {"id": 1, "title": "Portfolio", "tags": ["fastapi", "vuejs3", "tailwindcss"]},
    {"id": 2, "title": "Cinema scraper", "tags": ["requests", "sqlmodel"]},
]


@router.get("")
def get_projects() -> list[dict]:
    return PROJECTS


@router.get("/{project_id}")
def get_project(project_id: int) -> dict:
    project = next((p for p in PROJECTS if p["id"] == project_id), None)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
