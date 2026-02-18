from datetime import UTC, datetime, timedelta

import jwt
from fastapi.testclient import TestClient

_SECRET = "testsecretkey-that-is-long-enough-for-hs512-needs-at-least-64-bytes-here"


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


def test_login_nonexistent_email(client: TestClient) -> None:
    response = client.post(
        "/api/auth/login",
        json={"email": "nobody@test.com", "password": "testpassword"},
    )
    assert response.status_code == 401


def test_me_with_expired_token(client: TestClient) -> None:
    expired_token = jwt.encode(
        {"sub": "admin@test.com", "exp": datetime.now(UTC) - timedelta(minutes=1)},
        _SECRET,
        algorithm="HS256",
    )
    response = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401


def test_me_with_invalid_token_format(client: TestClient) -> None:
    response = client.get(
        "/api/auth/me", headers={"Authorization": "Bearer notavalidtoken"}
    )
    assert response.status_code == 401


def test_me_with_wrong_algorithm_token(client: TestClient) -> None:
    wrong_algo_token = jwt.encode(
        {"sub": "admin@test.com"},
        _SECRET,
        algorithm="HS512",
    )
    response = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {wrong_algo_token}"}
    )
    assert response.status_code == 401
