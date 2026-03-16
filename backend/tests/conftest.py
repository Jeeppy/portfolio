from collections.abc import Generator
from datetime import date, time, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import app.uploads as file_uploads
from app.auth import get_current_admin, get_optional_admin
from app.config import Settings, get_settings
from app.database import get_session
from app.main import app
from app.models import (  # noqa: F401
    Appointment,
    AvailabilitySlot,
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
        secret_key="testsecretkey-that-is-long-enough-for-hs256",  # gitleaks:allow
        database_url="sqlite://",
    )
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield
    app.dependency_overrides.pop(get_settings, None)


@pytest.fixture
def message(session: Session) -> ContactMessage:
    message = ContactMessage(
        name="first", email="first@test.com", subject="sub 1", message="message 1"
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


@pytest.fixture
def education(session: Session) -> Education:
    profile = Profile()
    session.add(profile)
    session.commit()
    session.refresh(profile)

    education = Education(
        school="MIT",
        degree="Bachelor",
        year=2022,
        profile_id=profile.id,
    )
    session.add(education)
    session.commit()
    session.refresh(education)

    return education


@pytest.fixture
def experience(session: Session) -> Experience:
    profile = Profile()
    session.add(profile)
    session.commit()
    session.refresh(profile)

    experience = Experience(
        company="Acme",
        position="backend developer",
        start_date=date(2022, 1, 1),
        profile_id=profile.id,
    )
    session.add(experience)
    session.commit()
    session.refresh(experience)

    return experience


@pytest.fixture
def project(session: Session) -> Project:
    project = Project(
        title="a new project",
        slug="a-new-project",
        description="a description for a new project",
        published=True,
    )
    session.add(project)
    project.tags.append(Tag(name="python"))
    project.tags.append(Tag(name="fastapi"))
    session.commit()
    session.refresh(project)
    return project


@pytest.fixture
def unpublished_project(session: Session) -> Project:
    unpublished = Project(
        title="draft",
        slug="draft",
        description="wip",
        published=False,
    )
    session.add(unpublished)
    session.commit()
    session.refresh(unpublished)
    return unpublished


@pytest.fixture
def skill(session: Session) -> Skill:
    profile = Profile()
    session.add(profile)
    session.commit()
    session.refresh(profile)

    skill = Skill(name="Python", category="Backend", level=9, profile_id=profile.id)
    session.add(skill)
    session.commit()
    session.refresh(skill)

    return skill


@pytest.fixture
def slot(session: Session) -> AvailabilitySlot:
    """Monday slot 09:00-10:00."""
    s = AvailabilitySlot(day_of_week=0, start_time=time(9, 0), end_time=time(10, 0))
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


@pytest.fixture
def appointment(session: Session) -> Appointment:
    a = Appointment(
        visitor_name="Bob",
        visitor_email="bob@example.com",
        appointment_date=date.today() + timedelta(days=7),
        start_time=time(10, 0),
        end_time=time(11, 0),
    )
    session.add(a)
    session.commit()
    session.refresh(a)
    return a


@pytest.fixture
def upload_dirs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(file_uploads, "AVATAR_DIR", tmp_path / "avatars")
    monkeypatch.setattr(file_uploads, "RESUME_DIR", tmp_path / "resumes")
