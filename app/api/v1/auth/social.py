# api/v1/auth/social.py
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api import deps
from app.schemas.auth.social_auth import (
    GoogleAuthRequest,
    FacebookAuthRequest,
    SocialAuthResponse,
)
from app.services.auth import SocialAuthService

router = APIRouter()


@router.post(
    "/google",
    response_model=SocialAuthResponse,
    status_code=status.HTTP_200_OK,
)
async def authenticate_with_google(
    payload: GoogleAuthRequest,
    social_auth_service: Annotated[SocialAuthService, Depends(deps.get_social_auth_service)],
) -> SocialAuthResponse:
    """
    Google social login.

    Currently a stub in the service layer and will raise NotImplementedError
    until the integration is implemented.
    """
    try:
        return social_auth_service.authenticate_with_google(payload)
    except NotImplementedError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth integration is not configured",
        )


@router.post(
    "/facebook",
    response_model=SocialAuthResponse,
    status_code=status.HTTP_200_OK,
)
async def authenticate_with_facebook(
    payload: FacebookAuthRequest,
    social_auth_service: Annotated[SocialAuthService, Depends(deps.get_social_auth_service)],
) -> SocialAuthResponse:
    """
    Facebook social login.

    Currently a stub in the service layer and will raise NotImplementedError
    until the integration is implemented.
    """
    try:
        return social_auth_service.authenticate_with_facebook(payload)
    except NotImplementedError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Facebook OAuth integration is not configured",
        )