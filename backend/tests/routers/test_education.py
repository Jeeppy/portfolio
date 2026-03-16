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


def test_list_education_sorted_by_year_descending(
    client: TestClient, education: Education, session: Session
) -> None:
    second_education = Education(
        school="Python school",
        degree="Bachelor",
        year=2023,
        profile_id=education.profile_id,
    )
    session.add(second_education)
    session.commit()

    response = client.get(EDUCATION_URL)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["school"] == "Python school"
    assert data[1]["school"] == "MIT"


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
