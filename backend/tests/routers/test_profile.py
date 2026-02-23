from fastapi.testclient import TestClient

PROFILE_URL = "/api/profile"


def test_get_profile_auto_create(client: TestClient) -> None:
    response = client.get(PROFILE_URL)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["full_name"] is None
    assert data["skills"] == []
