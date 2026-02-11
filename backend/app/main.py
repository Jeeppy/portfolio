from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.config import get_settings
from app.database import init_db
from app.logging import setup_logging
from app.routers import auth, contact, profile, projects

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Exécuté au démarrage / arrêt de l'app."""
    setup_logging(debug=settings.debug)
    logger = structlog.get_logger()
    logger.info("Starting Portfolio API", debug=settings.debug)
    init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down")


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.include_router(projects.router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(profile.router, prefix=settings.api_prefix)
app.include_router(contact.router, prefix=settings.api_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello Portfolio!"}
