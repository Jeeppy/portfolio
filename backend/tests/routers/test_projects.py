from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Project

PROJECTS_URL = "api/projects"


def test_list_projects_empty(client: TestClient) -> None:
    response = client.get(PROJECTS_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_list_projects_hides_unpublished(
    client: TestClient, project: Project, unpublished_project: Project, session: Session
) -> None:
    response = client.get(PROJECTS_URL)
    assert response.status_code == 200
    slugs = [p["slug"] for p in response.json()]
    assert "a-new-project" in slugs
    assert "draft" not in slugs


def test_list_projects_pagination(admin_client: TestClient, session: Session) -> None:
    for i in range(5):
        session.add(
            Project(
                title=f"Project{i}",
                slug=f"project-{i}",
                description="desc",
                published=True,
            )
        )
    session.commit()

    response = admin_client.get(f"{PROJECTS_URL}?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = admin_client.get(f"{PROJECTS_URL}?offset=3")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_project_by_slug(admin_client: TestClient, project: Project) -> None:
    response = admin_client.get(f"{PROJECTS_URL}/a-new-project")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == project.title
    assert data["description"] == project.description
    assert data["published"] is True


def test_get_project_not_found(client: TestClient) -> None:
    response = client.get(f"{PROJECTS_URL}/nope")
    assert response.status_code == 404


def test_get_project_not_published(
    client: TestClient, unpublished_project: Project, session: Session
) -> None:
    response = client.get(f"{PROJECTS_URL}/draft")
    assert response.status_code == 404
