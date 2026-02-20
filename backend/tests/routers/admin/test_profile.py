from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Skill

ADMIN_PROFILE_URL = "/api/admin/profile"


def test_update_profile(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "full_name": "Jean-Pierre",
            "title": "Développeur",
            "bio": "Hello world",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jean-Pierre"
    assert data["title"] == "Développeur"
    assert data["bio"] == "Hello world"


def test_update_profile_with_skills(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "skills": [
                {"name": "Python", "category": "backend", "level": 5},
                {"name": "FastAPI", "category": "backend", "level": 4},
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["skills"]) == 2
    assert data["skills"][0]["name"] == "Python"
    assert data["skills"][1]["level"] == 4


def test_update_profile_replaces_skills(admin_client: TestClient) -> None:
    admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "skills": [{"name": "Python", "category": "backend", "level": 5}],
        },
    )

    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "skills": [{"name": "Go", "category": "backend", "level": 3}],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["skills"]) == 1
    assert data["skills"][0]["name"] == "Go"


def test_update_profile_with_experiences(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "experiences": [
                {
                    "company": "Acme",
                    "position": "Dev",
                    "start_date": "2023-01-01",
                    "end_date": "2024-06-30",
                },
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["experiences"]) == 1
    assert data["experiences"][0]["company"] == "Acme"


def test_update_profile_with_education(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "education": [
                {"school": "MIT", "degree": "CS", "year": 2020},
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["education"]) == 1
    assert data["education"][0]["school"] == "MIT"


def test_update_profile_without_auth(client: TestClient) -> None:
    response = client.put(ADMIN_PROFILE_URL, json={"full_name": "Nope"})

    assert response.status_code == 401


def test_update_profile_partial_update(admin_client: TestClient) -> None:
    admin_client.put(ADMIN_PROFILE_URL, json={"full_name": "Jean", "title": "Dev"})

    response = admin_client.put(ADMIN_PROFILE_URL, json={"bio": "new bio"})

    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "new bio"
    assert data["full_name"] == "Jean"


def test_update_profile_invalid_skill_level(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={"skills": [{"name": "Python", "category": "backend", "level": -1}]},
    )
    assert response.status_code == 422

    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={"skills": [{"name": "Python", "category": "backend", "level": 11}]},
    )
    assert response.status_code == 422


def test_update_profile_cascade_deletes_skills(
    admin_client: TestClient, session: Session
) -> None:
    admin_client.put(
        ADMIN_PROFILE_URL,
        json={"skills": [{"name": "Python", "category": "backend", "level": 5}]},
    )
    session.expire_all()
    assert len(session.exec(select(Skill)).all()) == 1

    admin_client.put(ADMIN_PROFILE_URL, json={"skills": []})
    session.expire_all()
    assert len(session.exec(select(Skill)).all()) == 0
