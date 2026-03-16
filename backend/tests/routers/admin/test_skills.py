from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Skill

ADMIN_SKILL_URL = "/api/admin/skills"


def test_create_skill(admin_client: TestClient, session: Session) -> None:
    response = admin_client.post(
        ADMIN_SKILL_URL, json={"name": "Git", "category": "Tools", "level": 7}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Git"
    assert data["category"] == "Tools"
    assert data["level"] == 7

    count = len(session.exec(select(Skill)).all())
    assert count == 1


def test_create_skill_without_auth(client: TestClient) -> None:
    response = client.post(
        ADMIN_SKILL_URL, json={"name": "Git", "category": "Tools", "level": 7}
    )
    assert response.status_code == 401


def test_create_skill_duplicate_skill(admin_client: TestClient, skill: Skill) -> None:
    response = admin_client.post(
        ADMIN_SKILL_URL, json={"name": "Python", "category": "Backend", "level": 7}
    )
    assert response.status_code == 409


def test_update_skill(admin_client: TestClient, skill: Skill) -> None:
    response = admin_client.put(
        f"{ADMIN_SKILL_URL}/{skill.id}", json={"category": "new category"}
    )
    assert response.status_code == 200
    assert response.json()["category"] == "new category"


def test_update_skill_not_found(admin_client: TestClient) -> None:
    response = admin_client.put(
        f"{ADMIN_SKILL_URL}/99", json={"category": "new category"}
    )
    assert response.status_code == 404


def test_update_skill_without_auth(client: TestClient, skill: Skill) -> None:
    response = client.put(
        f"{ADMIN_SKILL_URL}/{skill.id}", json={"category": "new category"}
    )
    assert response.status_code == 401


def test_delete_skill(admin_client: TestClient, skill: Skill, session: Session) -> None:
    response = admin_client.delete(f"{ADMIN_SKILL_URL}/{skill.id}")
    assert response.status_code == 204
    assert session.get(Skill, skill.id) is None


def test_delete_skill_not_found(admin_client: TestClient) -> None:
    response = admin_client.delete(f"{ADMIN_SKILL_URL}/55")
    assert response.status_code == 404


def test_delete_skill_without_auth(client: TestClient, skill: Skill) -> None:
    response = client.delete(f"{ADMIN_SKILL_URL}/{skill.id}")
    assert response.status_code == 401
