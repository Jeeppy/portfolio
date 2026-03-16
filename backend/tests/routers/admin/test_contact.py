from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import ContactMessage

ADMIN_CONTACT_URL = "/api/admin/contact"


def test_list_messages_admin(
    admin_client: TestClient, client: TestClient, session: Session
) -> None:
    session.add(
        ContactMessage(
            name="first",
            email="first@test.com",
            subject="sub1",
            message="msg1",
        )
    )
    session.add(
        ContactMessage(
            name="second",
            email="second@test.com",
            subject="sub2",
            message="msg2",
        )
    )

    response = admin_client.get(ADMIN_CONTACT_URL)
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "second"
    assert data[1]["name"] == "first"
    assert "id" in data[0]
    assert "read" in data[0]
    assert "created_at" in data[0]


def test_list_messages_without_auth(client: TestClient) -> None:
    response = client.get(ADMIN_CONTACT_URL)
    assert response.status_code == 401


def test_list_messages_filter_unread(
    admin_client: TestClient, session: Session
) -> None:
    session.add(
        ContactMessage(
            name="a", email="a@test.com", subject="s", message="m", read=True
        )
    )
    session.add(
        ContactMessage(
            name="b", email="b@test.com", subject="s", message="m", read=False
        )
    )
    session.commit()

    response = admin_client.get(f"{ADMIN_CONTACT_URL}?read=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "b"


def test_list_messages_filter_read(admin_client: TestClient, session: Session) -> None:
    session.add(
        ContactMessage(
            name="a", email="a@test.com", subject="s", message="m", read=True
        )
    )
    session.add(
        ContactMessage(
            name="b", email="b@test.com", subject="s", message="m", read=False
        )
    )
    session.commit()

    response = admin_client.get(f"{ADMIN_CONTACT_URL}?read=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "a"


def test_mark_as_read(
    session: Session,
    admin_client: TestClient,
    client: TestClient,
    message: ContactMessage,
) -> None:
    response = admin_client.patch(f"{ADMIN_CONTACT_URL}/{message.id}/read")
    assert response.status_code == 200
    assert message.read is True


def test_mark_as_read_not_found(admin_client: TestClient) -> None:
    response = admin_client.patch(f"{ADMIN_CONTACT_URL}/999/read")
    assert response.status_code == 404


def test_delete_message(admin_client: TestClient, message: ContactMessage) -> None:
    response = admin_client.delete(f"{ADMIN_CONTACT_URL}/{message.id}")
    assert response.status_code == 204


def test_deleted_message_hidden_from_list(
    admin_client: TestClient, message: ContactMessage
) -> None:
    admin_client.delete(f"{ADMIN_CONTACT_URL}/{message.id}")
    response = admin_client.get(ADMIN_CONTACT_URL)
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_delete_message_not_found(admin_client: TestClient) -> None:
    response = admin_client.delete(f"{ADMIN_CONTACT_URL}/999")
    assert response.status_code == 404


def test_delete_message_without_auth(
    client: TestClient, message: ContactMessage
) -> None:
    response = client.delete(f"{ADMIN_CONTACT_URL}/{message.id}")
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

    response = admin_client.get(f"{ADMIN_CONTACT_URL}?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


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

        response = admin_client.get(f"{ADMIN_CONTACT_URL}?offset=10")
        assert response.status_code == 200
        assert response.json() == []
