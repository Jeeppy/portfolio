from datetime import time

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import AvailabilitySlot

ADMIN_AVAILABILITY_URL = "/api/admin/availability"


def test_create_availability_slot(admin_client: TestClient) -> None:
    response = admin_client.post(
        ADMIN_AVAILABILITY_URL,
        json={
            "day_of_week": 1,
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "is_active": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["day_of_week"] == 1


def test_list_availability_slots(admin_client: TestClient, session: Session) -> None:
    session.add(
        AvailabilitySlot(day_of_week=2, start_time=time(14, 0), end_time=time(15, 0))
    )
    session.commit()

    response = admin_client.get(ADMIN_AVAILABILITY_URL)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_availability_slot(admin_client: TestClient, session: Session) -> None:
    slot = AvailabilitySlot(day_of_week=3, start_time=time(8, 0), end_time=time(9, 0))
    session.add(slot)
    session.commit()
    session.refresh(slot)

    response = admin_client.delete(f"{ADMIN_AVAILABILITY_URL}/{slot.id}")

    assert response.status_code == 204


def test_delete_availability_slot_not_found(admin_client: TestClient) -> None:
    response = admin_client.delete(f"{ADMIN_AVAILABILITY_URL}/9999")

    assert response.status_code == 404


def test_availability_requires_auth(client: TestClient) -> None:
    response = client.post(
        ADMIN_AVAILABILITY_URL,
        json={
            "day_of_week": 1,
            "start_time": "10:00:00",
            "end_time": "11:00:00",
        },
    )

    assert response.status_code == 401
