from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import ProjectCategory

ADMIN_CATEGORIES_URL = "/api/admin/categories"


def test_create_category(admin_client: TestClient, session: Session) -> None:
    response = admin_client.post(
        ADMIN_CATEGORIES_URL,
        json={"name": "Web", "slug": "web"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Web"
    assert data["slug"] == "web"


def test_create_category_duplicate(admin_client: TestClient) -> None:
    admin_client.post(ADMIN_CATEGORIES_URL, json={"name": "Web", "slug": "web"})
    response = admin_client.post(
        ADMIN_CATEGORIES_URL, json={"name": "Web", "slug": "web"}
    )
    assert response.status_code == 409


def test_create_category_without_auth(client: TestClient) -> None:
    response = client.post(ADMIN_CATEGORIES_URL, json={"name": "Web", "slug": "web"})
    assert response.status_code == 401


def test_list_categories(admin_client: TestClient) -> None:
    admin_client.post(ADMIN_CATEGORIES_URL, json={"name": "Web", "slug": "web"})
    admin_client.post(ADMIN_CATEGORIES_URL, json={"name": "API", "slug": "api"})

    response = admin_client.get(ADMIN_CATEGORIES_URL)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_categories_without_auth(client: TestClient) -> None:
    response = client.get(ADMIN_CATEGORIES_URL)
    assert response.status_code == 401


def test_delete_category(admin_client: TestClient, session: Session) -> None:
    admin_client.post(ADMIN_CATEGORIES_URL, json={"name": "Web", "slug": "web"})

    response = admin_client.delete(f"{ADMIN_CATEGORIES_URL}/web")
    assert response.status_code == 204
    assert session.get(ProjectCategory, 1) is None


def test_delete_category_not_found(admin_client: TestClient) -> None:
    response = admin_client.delete(f"{ADMIN_CATEGORIES_URL}/nonexistent")
    assert response.status_code == 404


def test_delete_category_without_auth(client: TestClient) -> None:
    response = client.delete(f"{ADMIN_CATEGORIES_URL}/web")
    assert response.status_code == 401
