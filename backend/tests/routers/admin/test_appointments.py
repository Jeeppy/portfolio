from fastapi.testclient import TestClient

from app.models import Appointment

ADMIN_APPOINTMENTS_URL = "/api/admin/appointments"


def test_list_appointments(admin_client: TestClient, appointment: Appointment) -> None:
    response = admin_client.get(ADMIN_APPOINTMENTS_URL)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_appointments_filter_by_status(
    admin_client: TestClient, appointment: Appointment
) -> None:
    response = admin_client.get(
        ADMIN_APPOINTMENTS_URL, params={"status_filter": "pending"}
    )
    assert len(response.json()) == 1

    response = admin_client.get(
        ADMIN_APPOINTMENTS_URL, params={"status_filter": "confirmed"}
    )
    assert len(response.json()) == 0


def test_update_appointment_status(
    admin_client: TestClient, appointment: Appointment
) -> None:
    response = admin_client.patch(
        f"{ADMIN_APPOINTMENTS_URL}/{appointment.id}/status",
        json={"status": "confirmed"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"


def test_update_appointment_status_invalid_transition(
    admin_client: TestClient, appointment: Appointment
) -> None:
    response = admin_client.patch(
        f"{ADMIN_APPOINTMENTS_URL}/{appointment.id}/status",
        json={"status": "cancelled"},
    )

    assert response.status_code == 422


def test_update_appointment_status_not_found(admin_client: TestClient) -> None:
    response = admin_client.patch(
        f"{ADMIN_APPOINTMENTS_URL}/9999/status",
        json={"status": "confirmed"},
    )

    assert response.status_code == 404


def test_delete_appointment(admin_client: TestClient, appointment: Appointment) -> None:
    response = admin_client.delete(f"{ADMIN_APPOINTMENTS_URL}/{appointment.id}")

    assert response.status_code == 204


def test_delete_appointment_not_found(admin_client: TestClient) -> None:
    response = admin_client.delete(f"{ADMIN_APPOINTMENTS_URL}/9999")

    assert response.status_code == 404


def test_appointments_requires_auth(
    client: TestClient, appointment: Appointment
) -> None:
    response = client.get(ADMIN_APPOINTMENTS_URL)

    assert response.status_code == 401
