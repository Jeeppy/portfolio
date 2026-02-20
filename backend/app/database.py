from collections.abc import Generator
from pathlib import Path

from sqlmodel import Session, create_engine

from app.config import get_settings

settings = get_settings()

# Create the data directory if it doesn't exist
db_path = settings.database_url.replace("sqlite:///", "")
Path(db_path).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False},
)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency - provide a DB session per request."""
    with Session(engine) as session:
        yield session
