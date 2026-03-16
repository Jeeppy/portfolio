from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Project, Tag

ADMIN_PROJECTS_URL = "api/admin/projects"


def test_list_all_projects(
    admin_client: TestClient, project: Project, unpublished_project: Project
) -> None:
    response = admin_client.get(ADMIN_PROJECTS_URL)
    assert response.status_code == 200
    slugs = [p["slug"] for p in response.json()]
    assert "a-new-project" in slugs
    assert "draft" in slugs


def test_list_all_projects_requires_auth(client: TestClient) -> None:
    response = client.get(ADMIN_PROJECTS_URL)
    assert response.status_code == 401


def test_list_projects_filter_by_category(
    client: TestClient, admin_client: TestClient, session: Session
) -> None:
    from app.models import ProjectCategory

    category = ProjectCategory(name="Web", slug="web")
    session.add(category)
    session.commit()
    session.refresh(category)

    session.add(
        Project(
            title="Web Project",
            slug="web-project",
            published=True,
            category_id=category.id,
        )
    )
    session.add(Project(title="Other Project", slug="other-project", published=True))
    session.commit()

    response = client.get("/api/projects?category=web")
    assert response.status_code == 200
    slugs = [p["slug"] for p in response.json()]
    assert "web-project" in slugs
    assert "other-project" not in slugs


def test_get_project(
    admin_client: TestClient, project: Project, session: Session
) -> None:
    response = admin_client.get(f"{ADMIN_PROJECTS_URL}/{project.slug}")

    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == project.slug
    assert data["title"] == project.title
    assert data["description"] == project.description
    assert data["published"] == project.published


def test_get_project_not_published(
    admin_client: TestClient, unpublished_project: Project, session: Session
) -> None:
    response = admin_client.get(f"{ADMIN_PROJECTS_URL}/{unpublished_project.slug}")

    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == unpublished_project.slug
    assert data["title"] == unpublished_project.title
    assert data["description"] == unpublished_project.description
    assert data["published"] == unpublished_project.published


def test_get_project_not_found(admin_client: TestClient) -> None:
    response = admin_client.get(f"{ADMIN_PROJECTS_URL}/not-found")
    assert response.status_code == 404


def test_get_project_without_auth(client: TestClient, project: Project) -> None:
    response = client.get(f"{ADMIN_PROJECTS_URL}/{project.slug}")
    assert response.status_code == 401


def test_create_project(admin_client: TestClient, session: Session) -> None:
    response = admin_client.post(
        ADMIN_PROJECTS_URL,
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
        ADMIN_PROJECTS_URL,
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
        ADMIN_PROJECTS_URL,
        json={
            "title": "good project",
            "slug": "a-new-project",
            "description": "a good project",
            "tags": ["python", "vuejs"],
            "published": True,
        },
    )
    assert response.status_code == 409


def test_create_project_slug_case_sensitivity(
    admin_client: TestClient, project: Project
) -> None:
    response = admin_client.post(
        ADMIN_PROJECTS_URL,
        json={
            "title": "Another project",
            "slug": "A-New-Project",
            "description": "same slug different case",
            "tags": [],
            "published": True,
        },
    )
    assert response.status_code in (201, 409)


def test_create_project_with_demo_url(
    admin_client: TestClient, session: Session
) -> None:
    response = admin_client.post(
        ADMIN_PROJECTS_URL,
        json={
            "title": "demo-project",
            "slug": "demo-project",
            "description": "a project with demo",
            "tags": [],
            "published": True,
            "demo_url": "https://demo.example.com",
        },
    )

    assert response.status_code == 201
    assert response.json()["demo_url"] == "https://demo.example.com"


def test_create_project_with_repository_url(
    admin_client: TestClient,
    session: Session,
) -> None:
    response = admin_client.post(
        ADMIN_PROJECTS_URL,
        json={
            "title": "repo-project",
            "slug": "repo-project",
            "description": "a project with a repo",
            "tags": [],
            "published": True,
            "repository_url": "https://github.com/user/repo",
        },
    )

    assert response.status_code == 201
    assert response.json()["repository_url"] == "https://github.com/user/repo"


def test_update_project(admin_client: TestClient, project: Project) -> None:
    response = admin_client.put(
        f"{ADMIN_PROJECTS_URL}/a-new-project", json={"description": "a new description"}
    )

    assert response.status_code == 200
    assert response.json()["description"] == "a new description"


def test_update_project_without_auth(client: TestClient, project: Project) -> None:
    response = client.put(
        f"{ADMIN_PROJECTS_URL}/a-new-project", json={"description": "nope"}
    )
    assert response.status_code == 401


def test_update_project_tags(admin_client: TestClient, project: Project) -> None:
    response = admin_client.put(
        f"{ADMIN_PROJECTS_URL}/a-new-project", json={"tags": ["django", "python"]}
    )

    assert response.status_code == 200
    tags = [t["name"] for t in response.json()["tags"]]
    assert "django" in tags
    assert "python" in tags
    assert "fastapi" not in tags


def test_update_project_not_found(admin_client: TestClient) -> None:
    response = admin_client.put(
        f"{ADMIN_PROJECTS_URL}/nonexistent", json={"description": "nope"}
    )
    assert response.status_code == 404


def test_update_project_tags_empty(admin_client: TestClient, project: Project) -> None:
    response = admin_client.put(
        f"{ADMIN_PROJECTS_URL}/a-new-project", json={"tags": []}
    )

    assert response.status_code == 200
    assert response.json()["tags"] == []


def test_update_project_demo_url(admin_client: TestClient, project: Project) -> None:
    response = admin_client.put(
        f"{ADMIN_PROJECTS_URL}/a-new-project",
        json={"demo_url": "https://demo.example.com"},
    )

    assert response.status_code == 200
    assert response.json()["demo_url"] == "https://demo.example.com"


def test_update_project_repository_url(
    admin_client: TestClient, project: Project
) -> None:
    response = admin_client.put(
        f"{ADMIN_PROJECTS_URL}/a-new-project",
        json={"repository_url": "https://github.com/user/repo"},
    )
    assert response.status_code == 200
    assert response.json()["repository_url"] == "https://github.com/user/repo"


def test_delete_project(admin_client: TestClient, project: Project) -> None:
    response = admin_client.delete(f"{ADMIN_PROJECTS_URL}/a-new-project")
    assert response.status_code == 204

    response = admin_client.get("/api/projects/a-new-project")
    assert response.status_code == 404


def test_delete_project_without_auth(client: TestClient, project: Project) -> None:
    response = client.delete(f"{ADMIN_PROJECTS_URL}/a-new-project")
    assert response.status_code == 401


def test_delete_project_not_found(admin_client: TestClient) -> None:
    response = admin_client.delete(f"{ADMIN_PROJECTS_URL}/nonexistent")
    assert response.status_code == 404
