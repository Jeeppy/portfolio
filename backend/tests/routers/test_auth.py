from fastapi.testclient import TestClient


def test_login_success(client: TestClient) -> None:
    response = client.post(
        "/api/auth/login", json={"email": "admin@test.com", "password": "testpassword"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient) -> None:
    response = client.post(
        "/api/auth/login",
        json={
            "email": "admin@test.com",
            "password": "badpassword",
        },
    )

    assert response.status_code == 401


def test_me_without_token(client: TestClient) -> None:
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_me_with_token(admin_client: TestClient) -> None:
    response = admin_client.get("/api/auth/me")

    assert response.status_code == 200
    assert response.json()["email"] == "admin@test.com"
