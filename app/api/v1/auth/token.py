# api/v1/auth/token.py
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from api import deps
from app.schemas.auth.token import (
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from app.services.auth import AuthService

router = APIRouter()


@router.post(
    "/token/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
)
async def refresh_access_token(
    payload: RefreshTokenRequest,
    auth_service: Annotated[AuthService, Depends(deps.get_auth_service)],
) -> RefreshTokenResponse:
    """
    Exchange a refresh token for a new access (and refresh) token.
    """
    return auth_service.refresh_token(payload)