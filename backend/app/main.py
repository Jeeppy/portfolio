from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

import app.uploads as file_uploads
from app.config import get_settings
from app.limiter import limiter
from app.logging import setup_logging
from app.routers import auth, contact, profile, projects
from app.routers.admin import categories as admin_categories
from app.routers.admin import contact as admin_contact
from app.routers.admin import profile as admin_profile
from app.routers.admin import projects as admin_projects

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Run on application startup / shutdown."""
    setup_logging(debug=settings.debug)
    logger = structlog.get_logger()
    logger.info("Starting Portfolio API", debug=settings.debug)
    yield
    logger.info("Shutting down")


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
file_uploads.AVATAR_DIR.mkdir(parents=True, exist_ok=True)
file_uploads.RESUME_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(projects.router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(profile.router, prefix=settings.api_prefix)
app.include_router(contact.router, prefix=settings.api_prefix)
app.include_router(admin_categories.router, prefix=settings.api_prefix)
app.include_router(admin_projects.router, prefix=settings.api_prefix)
app.include_router(admin_profile.router, prefix=settings.api_prefix)
app.include_router(admin_contact.router, prefix=settings.api_prefix)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger = structlog.get_logger()
    logger.error("unhandled_exception", exc_info=exc, path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Returns API health status."""
    return {"status": "ok"}
