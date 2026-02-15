from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.auth import get_current_admin, get_optional_admin
from app.config import Settings, get_settings
from app.database import get_session
from app.main import app
from app.models import (  # noqa: F401
    ContactMessage,
    Education,
    Experience,
    Profile,
    Project,
    ProjectTagLink,
    Skill,
    Tag,
)


@pytest.fixture
def session() -> Generator[Session]:
    """In-memory DB - recreated for each test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(session: Session) -> Generator[TestClient]:
    """HTTP client using the test DB."""
    app.dependency_overrides[get_session] = lambda: session
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def admin_client(client: TestClient) -> Generator[TestClient]:
    """Authenticated client (admin)."""

    def _fake_admin() -> str:
        return "admin@test.com"

    app.dependency_overrides[get_current_admin] = _fake_admin
    app.dependency_overrides[get_optional_admin] = _fake_admin
    try:
        yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def settings_override() -> Generator[None]:
    """Override settings for tests."""
    test_settings = Settings(
        admin_email="admin@test.com",
        admin_password="testpassword",
        secret_key="test-secret-key",
        database_url="sqlite://",
    )
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield
    app.dependency_overrides.pop(get_settings, None)
