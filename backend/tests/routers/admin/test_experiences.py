from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Experience

ADMIN_EXPERIENCE_URL = "/api/admin/experiences"


def test_create_experience(admin_client: TestClient, session: Session) -> None:
    response = admin_client.post(
        ADMIN_EXPERIENCE_URL,
        json={
            "company": "python company",
            "position": "developer",
            "start_date": "2022-01-01",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["company"] == "python company"
    assert data["position"] == "developer"
    assert data["start_date"] == "2022-01-01"

    count = len(session.exec(select(Experience)).all())
    assert count == 1


def test_create_experience_without_auth(client: TestClient) -> None:
    response = client.post(
        ADMIN_EXPERIENCE_URL,
        json={
            "company": "python company",
            "position": "developer",
            "start_date": "2022-01-01",
        },
    )
    assert response.status_code == 401


def test_update_experience(admin_client: TestClient, experience: Experience) -> None:
    response = admin_client.put(
        f"{ADMIN_EXPERIENCE_URL}/{experience.id}", json={"position": "dev ops"}
    )
    assert response.status_code == 200
    assert response.json()["position"] == "dev ops"


def test_update_experience_not_found(admin_client: TestClient) -> None:
    response = admin_client.put(
        f"{ADMIN_EXPERIENCE_URL}/99", json={"position": "dev ops"}
    )
    assert response.status_code == 404


def test_update_experience_without_auth(
    client: TestClient, experience: Experience
) -> None:
    response = client.put(
        f"{ADMIN_EXPERIENCE_URL}/{experience.id}", json={"position": "dev ops"}
    )
    assert response.status_code == 401


def test_delete_experience(
    admin_client: TestClient, experience: Experience, session: Session
) -> None:
    response = admin_client.delete(f"{ADMIN_EXPERIENCE_URL}/{experience.id}")
    assert response.status_code == 204
    assert session.get(Experience, experience.id) is None


def test_delete_experience_not_found(admin_client: TestClient) -> None:
    response = admin_client.delete(f"{ADMIN_EXPERIENCE_URL}/55")
    assert response.status_code == 404


def test_delete_experience_without_auth(
    client: TestClient, experience: Experience
) -> None:
    response = client.delete(f"{ADMIN_EXPERIENCE_URL}/{experience.id}")
    assert response.status_code == 401
