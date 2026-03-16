from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import ContactMessage

CONTACT_URL = "/api/contact"


def test_send_message(client: TestClient, session: Session) -> None:
    response = client.post(
        CONTACT_URL,
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


def test_create_message_rate_limited(client: TestClient) -> None:
    payload = {
        "name": "spam",
        "email": "spam@test.com",
        "subject": "spam",
        "message": "spam message",
    }
    for _ in range(5):
        client.post(f"{CONTACT_URL}/", json=payload)

    response = client.post(f"{CONTACT_URL}/", json=payload)
    assert response.status_code == 429


def test_send_message_invalid_email(client: TestClient) -> None:
    response = client.post(
        CONTACT_URL,
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
        f"{CONTACT_URL}/",
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
        CONTACT_URL,
        json={
            "name": "a person",
            "email": "mail@test.com",
            "subject": "a subject",
            "message": "a" * 5001,
        },
    )
    assert response.status_code == 422
