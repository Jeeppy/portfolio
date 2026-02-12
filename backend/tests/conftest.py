from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.auth import get_current_admin
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
    """DB en mémoire - recréée pour chaque test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session) -> Generator[TestClient]:
    """Client HTTP qui utilise la DB de test."""

    def _get_test_session() -> Generator[Session]:
        yield session

    app.dependency_overrides[get_session] = _get_test_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_client(client: TestClient) -> Generator[TestClient]:
    """Client authentifié (admin)"""

    def _fake_admin() -> str:
        return "admin@test.com"

    app.dependency_overrides[get_current_admin] = _fake_admin
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def settings_override() -> Generator[None]:
    """Override settings pour les tests."""
    test_settings = Settings(
        admin_email="admin@test.com",
        admin_password="testpassword",
        secret_key="test-secret-key",
        database_url="sqlite://",
    )
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield
    app.dependency_overrides.pop(get_settings, None)
