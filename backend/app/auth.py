from datetime import UTC, datetime, timedelta

import bcrypt
import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import Settings, get_settings

security = HTTPBearer()
logger = structlog.get_logger()


def verify_password(plain: str, hashed: str) -> bool:
    """Vérifie un mot de passe contre son hash."""
    result: bool = bcrypt.checkpw(plain.encode(), hashed.encode())
    return result


def hash_password(password: str) -> str:
    """Hash un mot de passe."""
    result: str = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return result


def create_access_token(data: dict, settings: Settings) -> str:
    """Créé un JWT avec une expiration."""
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
    """Vérifier le JWT et retourne l'email admin."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
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
