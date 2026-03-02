import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Profile, Skill

SKILL_URL = "api/skills"


@pytest.fixture
def skill(session: Session) -> Skill:
    profile = Profile()
    session.add(profile)
    session.commit()
    session.refresh(profile)

    skill = Skill(name="Python", category="Backend", level=9, profile_id=profile.id)
    session.add(skill)
    session.commit()
    session.refresh(skill)

    return skill


def test_list_skill_empty(client: TestClient) -> None:
    response = client.get(SKILL_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_list_skills(client: TestClient, skill: Skill, session: Session) -> None:
    response = client.get(SKILL_URL)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Python"
    assert data[0]["category"] == "Backend"
    assert data[0]["level"] == 9
