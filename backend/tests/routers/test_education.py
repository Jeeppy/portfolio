import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Education, Profile

EDUCATION_URL = "/api/education"


@pytest.fixture
def education(session: Session) -> Education:
    profile = Profile()
    session.add(profile)
    session.commit()
    session.refresh(profile)

    education = Education(
        school="MIT",
        degree="Bachelor",
        year=2022,
        profile_id=profile.id,
    )
    session.add(education)
    session.commit()
    session.refresh(education)

    return education


def test_list_education_empty(client: TestClient) -> None:
    response = client.get(EDUCATION_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_list_education(client: TestClient, education: Education) -> None:
    response = client.get(EDUCATION_URL)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["school"] == "MIT"
    assert data[0]["degree"] == "Bachelor"
    assert data[0]["year"] == 2022


def test_get_education(client: TestClient, education: Education) -> None:
    response = client.get(f"{EDUCATION_URL}/{education.id}")

    assert response.status_code == 200
    data = response.json()

    assert data["school"] == education.school
    assert data["degree"] == education.degree
    assert data["year"] == education.year


def test_get_education_not_exist(client: TestClient) -> None:
    response = client.get(f"{EDUCATION_URL}/99")
    assert response.status_code == 404
