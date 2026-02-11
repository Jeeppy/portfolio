from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import (
    create_access_token,
    get_current_admin,
    hash_password,
    verify_password,
)
from app.config import get_settings
from app.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

# Hash the admin password only once at startup
_admin_hash: str = hash_password(settings.admin_password)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest) -> TokenResponse:
    if settings.admin_email != data.email or not verify_password(
        data.password, _admin_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    access_token = create_access_token({"sub": data.email})
    return TokenResponse(access_token=access_token)


@router.get("/me")
def me(email: str = Depends(get_current_admin)) -> dict[str, str]:
    return {"email": email}
