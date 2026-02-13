from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import Settings, get_settings

security = HTTPBearer()
logger = structlog.get_logger()
bearer_optional = HTTPBearer(auto_error=False)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    result: bool = bcrypt.checkpw(plain.encode(), hashed.encode())
    return result


def hash_password(password: str) -> str:
    """Hash a password."""
    result: str = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return result


def create_access_token(data: dict, settings: Settings) -> str:
    """Create a JWT with an expiration."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    token: str = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return token


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    settings: Settings = Depends(get_settings),
) -> str:
    """Verify the JWT and return the admin email."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as error:
        logger.warning("Invalid or expired token")
        raise credentials_exception from error
    return email


def get_optional_admin(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(bearer_optional)
    ] = None,
    settings: Settings = Depends(get_settings),
) -> str | None:
    if credentials is None:
        return None
    return get_current_admin(credentials, settings)
