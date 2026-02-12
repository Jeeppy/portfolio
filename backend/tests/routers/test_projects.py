import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Project, Tag


@pytest.fixture
def project(session: Session) -> Project:
    project = Project(
        title="a new project",
        slug="a-new-project",
        description="a description for a new project",
        published=True,
    )
    session.add(project)
    project.tags.append(Tag(name="python"))
    project.tags.append(Tag(name="fastapi"))
    session.commit()
    session.refresh(project)
    return project


def test_list_projects_empty(client: TestClient) -> None:
    response = client.get("/api/projects")

    assert response.status_code == 200
    assert response.json() == []


def test_create_project(admin_client: TestClient, session: Session) -> None:
    response = admin_client.post(
        "/api/projects",
        json={
            "title": "good project",
            "slug": "a-good-project",
            "description": "a good project",
            "tags": ["python", "vuejs"],
            "published": True,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["slug"] == "a-good-project"
    assert data["title"] == "good project"
    assert data["id"] is not None
    assert len(data["tags"]) == 2

    projects = session.exec(select(Project)).all()
    tags = session.exec(select(Tag)).all()
    assert len(projects) == 1
    assert len(tags) == 2


def test_create_project_without_auth(client: TestClient) -> None:
    response = client.post(
        "/api/projects",
        json={
            "title": "good project",
            "slug": "a-good-project",
            "description": "a good project",
            "tags": ["python", "vuejs"],
            "published": True,
        },
    )

    assert response.status_code == 401


def test_create_duplicate_slug(admin_client: TestClient, project: Project) -> None:
    response = admin_client.post(
        "/api/projects",
        json={
            "title": "good project",
            "slug": "a-new-project",
            "description": "a good project",
            "tags": ["python", "vuejs"],
            "published": True,
        },
    )
    assert response.status_code == 409


def test_get_project_by_slug(admin_client: TestClient, project: Project) -> None:
    response = admin_client.get("/api/projects/a-new-project")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "a new project"
    assert data["description"] == "a description for a new project"
    assert data["published"] is True


def test_get_project_not_found(client: TestClient) -> None:
    response = client.get("/api/projects/nope")
    assert response.status_code == 404


def test_update_project(admin_client: TestClient, project: Project) -> None:
    response = admin_client.put(
        "/api/projects/a-new-project", json={"description": "a new description"}
    )

    assert response.status_code == 200
    assert response.json()["description"] == "a new description"


def test_update_project_tags(admin_client: TestClient, project: Project) -> None:
    response = admin_client.put(
        "/api/projects/a-new-project", json={"tags": ["django", "python"]}
    )

    assert response.status_code == 200
    tags = [t["name"] for t in response.json()["tags"]]
    assert "django" in tags
    assert "python" in tags
    assert "fastapi" not in tags


def test_delete_project(admin_client: TestClient, project: Project) -> None:
    response = admin_client.delete("/api/projects/a-new-project")
    assert response.status_code == 204

    response = admin_client.get("/api/projects/a-new-project")
    assert response.status_code == 404
