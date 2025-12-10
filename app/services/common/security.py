# app/services/common/security.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.schemas.common.enums import UserRole


_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True)
class JWTSettings:
    """
    Runtime JWT configuration.

    Typically instantiated from environment / settings, e.g.:

        jwt_settings = JWTSettings(
            secret_key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
            access_token_expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expires_days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        )
    """
    secret_key: str
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 60  # default 1 hour
    refresh_token_expires_days: int = 30


# ------------------------------------------------------------------ #
# Password hashing
# ------------------------------------------------------------------ #
def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored hash."""
    return _pwd_context.verify(plain_password, hashed_password)


# ------------------------------------------------------------------ #
# JWT helpers
# ------------------------------------------------------------------ #
def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TokenDecodeError(Exception):
    """Raised when token decoding fails."""


def create_access_token(
    *,
    subject: UUID,
    email: str,
    role: UserRole,
    jwt_settings: JWTSettings,
    additional_claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a signed JWT access token.

    :param subject: User ID
    :param email: User email
    :param role: User role
    :param jwt_settings: JWT configuration
    :param additional_claims: optional extra claims to embed
    :param expires_delta: custom expiry (overrides default)
    """
    now = _utcnow()
    if expires_delta is None:
        expires_delta = timedelta(minutes=jwt_settings.access_token_expires_minutes)
    expire = now + expires_delta

    payload: Dict[str, Any] = {
        "sub": str(subject),
        "user_id": str(subject),
        "email": email,
        "role": role.value,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "access",
    }
    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(payload, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)


def create_refresh_token(
    *,
    subject: UUID,
    jwt_settings: JWTSettings,
    additional_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Create a signed JWT refresh token.
    """
    now = _utcnow()
    expire = now + timedelta(days=jwt_settings.refresh_token_expires_days)

    payload: Dict[str, Any] = {
        "sub": str(subject),
        "user_id": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "refresh",
    }
    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(payload, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)


def decode_token(token: str, jwt_settings: JWTSettings) -> Dict[str, Any]:
    """
    Decode a JWT and return its payload.

    Raises TokenDecodeError when invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            jwt_settings.secret_key,
            algorithms=[jwt_settings.algorithm],
        )
        return payload
    except JWTError as exc:
        raise TokenDecodeError("Invalid or expired token") from exc