from datetime import date, time

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Appointment, AvailabilitySlot

APPOINTMENTS_URL = "/api/appointments"
AVAILABLE_URL = "/api/appointments/available"


@pytest.fixture
def slot(session: Session) -> AvailabilitySlot:
    """Monday slot 09:00-10:00."""
    s = AvailabilitySlot(day_of_week=0, start_time=time(9, 0), end_time=time(10, 0))
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


def next_weekday(weekday: int) -> date:
    """Return the next date matching the given weekday (0=Monday)."""
    from datetime import timedelta

    today = date.today()
    days_ahead = (weekday - today.weekday()) % 7 or 7
    return today + timedelta(days=days_ahead)


def test_get_available_slots(client: TestClient, slot: AvailabilitySlot) -> None:
    next_monday = next_weekday(0)
    response = client.get(AVAILABLE_URL, params={"appointment_date": str(next_monday)})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["day_of_week"] == 0


def test_get_available_slots_excludes_booked(
    client: TestClient, slot: AvailabilitySlot, session: Session
) -> None:
    next_monday = next_weekday(0)
    booked = Appointment(
        visitor_name="Alice",
        visitor_email="alice@example.com",
        appointment_date=next_monday,
        start_time=time(9, 0),
        end_time=time(10, 0),
        status="confirmed",
    )
    session.add(booked)
    session.commit()

    response = client.get(AVAILABLE_URL, params={"appointment_date": str(next_monday)})

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_available_slots_inactive_excluded(
    client: TestClient, session: Session
) -> None:
    next_monday = next_weekday(0)
    inactive = AvailabilitySlot(
        day_of_week=0, start_time=time(11, 0), end_time=time(12, 0), is_active=False
    )
    session.add(inactive)
    session.commit()

    response = client.get(AVAILABLE_URL, params={"appointment_date": str(next_monday)})

    assert response.status_code == 200
    assert all(s["is_active"] for s in response.json())


def test_create_appointment(client: TestClient, slot: AvailabilitySlot) -> None:
    next_monday = next_weekday(0)
    response = client.post(
        APPOINTMENTS_URL,
        json={
            "visitor_name": "Alice",
            "visitor_email": "alice@example.com",
            "appointment_date": str(next_monday),
            "start_time": "09:00:00",
            "end_time": "10:00:00",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["visitor_name"] == "Alice"
    assert data["status"] == "pending"


def test_create_appointment_past_date(client: TestClient) -> None:
    response = client.post(
        APPOINTMENTS_URL,
        json={
            "visitor_name": "Alice",
            "visitor_email": "alice@example.com",
            "appointment_date": "2020-01-01",
            "start_time": "09:00:00",
            "end_time": "10:00:00",
        },
    )

    assert response.status_code == 422


def test_create_appointment_double_booking(
    client: TestClient, slot: AvailabilitySlot
) -> None:
    next_monday = next_weekday(0)
    payload = {
        "visitor_name": "Alice",
        "visitor_email": "alice@example.com",
        "appointment_date": str(next_monday),
        "start_time": "09:00:00",
        "end_time": "10:00:00",
    }
    client.post(APPOINTMENTS_URL, json=payload)
    response = client.post(APPOINTMENTS_URL, json=payload)

    assert response.status_code == 409
