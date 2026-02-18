import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import ContactMessage


@pytest.fixture
def message(session: Session) -> ContactMessage:
    message = ContactMessage(
        name="first", email="first@test.com", subject="sub 1", message="message 1"
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


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
    session: Session,
    admin_client: TestClient,
    client: TestClient,
    message: ContactMessage,
) -> None:
    response = admin_client.patch(f"/api/contact/{message.id}/read")
    assert response.status_code == 200
    assert message.read is True


def test_mark_as_read_not_found(admin_client: TestClient) -> None:
    response = admin_client.patch("/api/contact/999/read")
    assert response.status_code == 404


def test_delete_message(admin_client: TestClient, message: ContactMessage) -> None:
    response = admin_client.delete(f"/api/contact/{message.id}")
    assert response.status_code == 204


def test_deleted_message_hidden_from_list(
    admin_client: TestClient, message: ContactMessage
) -> None:
    admin_client.delete(f"/api/contact/{message.id}")
    response = admin_client.get("/api/contact")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_delete_message_not_found(admin_client: TestClient) -> None:
    response = admin_client.delete("/api/contact/999")
    assert response.status_code == 404


def test_delete_message_without_auth(
    client: TestClient, message: ContactMessage
) -> None:
    response = client.delete(f"/api/contact/{message.id}")
    assert response.status_code == 401


def test_list_messages_pagination(admin_client: TestClient, session: Session) -> None:
    for i in range(5):
        session.add(
            ContactMessage(
                name=f"user{i}",
                email=f"u{i}@test.com",
                subject="sub",
                message="msg",
            )
        )
    session.commit()

    response = admin_client.get("/api/contact?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_create_message_rate_limited(client: TestClient) -> None:
    payload = {
        "name": "spam",
        "email": "spam@test.com",
        "subject": "spam",
        "message": "spam message",
    }
    for _ in range(5):
        client.post("/api/contact/", json=payload)

    response = client.post("/api/contact/", json=payload)
    assert response.status_code == 429


def test_send_message_invalid_email(client: TestClient) -> None:
    response = client.post(
        "/api/contact",
        json={
            "name": "a person",
            "email": "not-an-email",
            "subject": "a subject",
            "message": "a message",
        },
    )
    assert response.status_code == 422


def test_send_message_whitespace_only(client: TestClient) -> None:
    response = client.post(
        "/api/contact/",
        json={
            "name": "    ",
            "email": "mail@test.com",
            "subject": "     ",
            "message": "     ",
        },
    )
    assert response.status_code == 422


def test_send_message_too_long(client: TestClient) -> None:
    response = client.post(
        "/api/contact",
        json={
            "name": "a person",
            "email": "mail@test.com",
            "subject": "a subject",
            "message": "a" * 5001,
        },
    )
    assert response.status_code == 422


def test_list_messages_pagination_offset_beyond_total(
    admin_client: TestClient, session: Session
) -> None:
    for i in range(3):
        session.add(
            ContactMessage(
                name=f"user{i}",
                email=f"u{i}@test.com",
                subject="sub",
                message="msg",
            )
        )
        session.commit()

        response = admin_client.get("/api/contact?offset=10")
        assert response.status_code == 200
        assert response.json() == []
