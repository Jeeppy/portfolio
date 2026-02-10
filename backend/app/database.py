from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False},
)


def init_db() -> None:
    """Crée les tables au démarrage."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency FastAPI - fournit une session DB par requête."""
    with Session(engine) as session:
        yield session
