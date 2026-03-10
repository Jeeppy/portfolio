from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Experience, Profile

EXPERIENCE_URL = "/api/experiences"


@pytest.fixture
def experience(session: Session) -> Experience:
    profile = Profile()
    session.add(profile)
    session.commit()
    session.refresh(profile)

    experience = Experience(
        company="Acme",
        position="backend developer",
        start_date=date(2022, 1, 1),
        profile_id=profile.id,
    )
    session.add(experience)
    session.commit()
    session.refresh(experience)

    return experience


def test_list_experience_empty(client: TestClient) -> None:
    response = client.get(EXPERIENCE_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_list_experiences(client: TestClient, experience: Experience) -> None:
    response = client.get(EXPERIENCE_URL)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Acme"
    assert data[0]["position"] == "backend developer"
    assert data[0]["start_date"] == "2022-01-01"


def test_get_experience(client: TestClient, experience: Experience) -> None:
    response = client.get(f"{EXPERIENCE_URL}/{experience.id}")

    assert response.status_code == 200
    data = response.json()

    assert data["company"] == experience.company
    assert data["position"] == experience.position
    assert data["start_date"] == experience.start_date.strftime("%Y-%m-%d")


def test_get_experience_not_exist(client: TestClient) -> None:
    response = client.get(f"{EXPERIENCE_URL}/99")
    assert response.status_code == 404
