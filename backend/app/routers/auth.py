import structlog
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import (
    create_access_token,
    get_current_admin,
    hash_password,
    verify_password,
)
from app.config import Settings, get_settings
from app.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])
logger = structlog.get_logger()

_admin_hash: str | None = None


def _get_admin_hash(settings: Settings) -> str:
    global _admin_hash
    if _admin_hash is None:
        _admin_hash = hash_password(settings.admin_password)
    return _admin_hash


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    admin_hash = _get_admin_hash(settings)
    if settings.admin_email != data.email or not verify_password(
        data.password, admin_hash
    ):
        logger.warning("Failed login attempt", email=data.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    access_token = create_access_token({"sub": data.email}, settings)
    logger.info("Admin logged in", email=data.email)
    return TokenResponse(access_token=access_token)


@router.get("/me")
def me(email: str = Depends(get_current_admin)) -> dict[str, str]:
    return {"email": email}
