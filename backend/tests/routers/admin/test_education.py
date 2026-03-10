import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Education, Profile

ADMIN_EDUCATION_URL = "/api/admin/education"


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


def test_create_education(admin_client: TestClient, session: Session) -> None:
    response = admin_client.post(
        ADMIN_EDUCATION_URL,
        json={
            "school": "MIT",
            "degree": "Bachelor",
            "year": 2022,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["school"] == "MIT"
    assert data["degree"] == "Bachelor"
    assert data["year"] == 2022

    count = len(session.exec(select(Education)).all())
    assert count == 1


def test_create_education_without_auth(client: TestClient) -> None:
    response = client.post(
        ADMIN_EDUCATION_URL,
        json={
            "school": "MIT",
            "degree": "Bachelor",
            "year": 2022,
        },
    )
    assert response.status_code == 401


def test_update_education(admin_client: TestClient, education: Education) -> None:
    response = admin_client.put(
        f"{ADMIN_EDUCATION_URL}/{education.id}", json={"degree": "master"}
    )
    assert response.status_code == 200
    assert response.json()["degree"] == "master"


def test_update_education_not_found(admin_client: TestClient) -> None:
    response = admin_client.put(f"{ADMIN_EDUCATION_URL}/99", json={"degree": "master"})
    assert response.status_code == 404


def test_update_education_without_auth(
    client: TestClient, education: Education
) -> None:
    response = client.put(
        f"{ADMIN_EDUCATION_URL}/{education.id}", json={"degree": "master"}
    )
    assert response.status_code == 401


def test_delete_education(
    admin_client: TestClient, education: Education, session: Session
) -> None:
    response = admin_client.delete(f"{ADMIN_EDUCATION_URL}/{education.id}")
    assert response.status_code == 204
    assert session.get(Education, education.id) is None


def test_delete_education_not_found(admin_client: TestClient) -> None:
    response = admin_client.delete(f"{ADMIN_EDUCATION_URL}/55")
    assert response.status_code == 404


def test_delete_education_without_auth(
    client: TestClient, education: Education
) -> None:
    response = client.delete(f"{ADMIN_EDUCATION_URL}/{education.id}")
    assert response.status_code == 401
