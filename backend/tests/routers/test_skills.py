from fastapi.testclient import TestClient

from app.models import Skill

SKILL_URL = "api/skills"


def test_list_skill_empty(client: TestClient) -> None:
    response = client.get(SKILL_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_list_skills(client: TestClient, skill: Skill) -> None:
    response = client.get(SKILL_URL)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Python"
    assert data[0]["category"] == "Backend"
    assert data[0]["level"] == 9


def test_get_skill(client: TestClient, skill: Skill) -> None:
    response = client.get(f"{SKILL_URL}/{skill.id}")

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == skill.name
    assert data["category"] == skill.category
    assert data["level"] == skill.level


def test_get_skill_not_exist(client: TestClient) -> None:
    response = client.get(f"{SKILL_URL}/99")
    assert response.status_code == 404
