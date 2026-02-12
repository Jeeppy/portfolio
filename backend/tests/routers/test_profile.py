from fastapi.testclient import TestClient


def test_get_profile_auto_create(client: TestClient) -> None:
    response = client.get("/api/profile")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["full_name"] == ""
    assert data["skills"] == []


def test_update_profile(admin_client: TestClient) -> None:
    response = admin_client.put(
        "/api/profile",
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
        "/api/profile",
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
        "/api/profile",
        json={
            "skills": [{"name": "Python", "category": "backend", "level": 5}],
        },
    )

    response = admin_client.put(
        "/api/profile",
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
        "/api/profile",
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
        "/api/profile",
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
    response = client.put("/api/profile", json={"full_name": "Nope"})

    assert response.status_code == 401
