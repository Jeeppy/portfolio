from fastapi import FastAPI, HTTPException

app = FastAPI(title="Portfolio API")

PROJECTS = [
    {"id": 1, "title": "Portfolio", "tags": ["fastapi", "vuejs3", "tailwindcss"]},
    {"id": 2, "title": "Cinema scraper", "tags": ["requests", "sqlmodel"]},
]


@app.get("/")
def root():
    return {"message:" "Hello Portfolio!"}


@app.get("/api/projects")
def get_projects():
    return PROJECTS


@app.get("/api/projects/{project_id}")
def get_project(project_id: int):
    project = next(
        (project for project in PROJECTS if project["id"] == project_id), None
    )

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project
