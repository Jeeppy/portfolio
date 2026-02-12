from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import ContactMessage


def test_send_message(client: TestClient, session: Session) -> None:
    response = client.post(
        "/api/contact",
        json={
            "name": "a person",
            "email": "mail@test.com",
            "subject": "a subject",
            "message": "a message",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "a person"
    assert data["email"] == "mail@test.com"
    assert data["subject"] == "a subject"
    assert data["message"] == "a message"

    msg = session.exec(select(ContactMessage)).first()
    assert msg is not None
    assert msg.email == "mail@test.com"
    assert msg.read is False


def test_list_messages_admin(admin_client: TestClient, client: TestClient) -> None:
    client.post(
        "/api/contact",
        json={
            "name": "first",
            "email": "first@test.com",
            "subject": "sub1",
            "message": "msg1",
        },
    )
    client.post(
        "/api/contact",
        json={
            "name": "second",
            "email": "second@test.com",
            "subject": "sub2",
            "message": "msg2",
        },
    )

    response = admin_client.get("/api/contact")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "first"
    assert data[1]["name"] == "second"
    assert "id" in data[0]
    assert "read" in data[0]
    assert "created_at" in data[0]


def test_list_messages_without_auth(client: TestClient) -> None:
    response = client.get("/api/contact")
    assert response.status_code == 401


def test_mark_as_read(
    session: Session, admin_client: TestClient, client: TestClient
) -> None:
    client.post(
        "/api/contact",
        json={
            "name": "first",
            "email": "first@test.com",
            "subject": "sub1",
            "message": "msg1",
        },
    )
    msg = session.exec(select(ContactMessage)).first()
    assert msg is not None
    response = admin_client.patch(f"/api/contact/{msg.id}/read")
    assert response.status_code == 200
    assert msg.read is True


def test_mark_as_read_not_found(admin_client: TestClient) -> None:
    response = admin_client.patch("/api/contact/999/read")
    assert response.status_code == 404
