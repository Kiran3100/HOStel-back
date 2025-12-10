# api/v1/auth/login.py
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api import deps
from app.schemas.auth.login import (
    LoginRequest,
    PhoneLoginRequest,
    LoginResponse,
)
from app.services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_with_email(
    payload: LoginRequest,
    request: Request,
    auth_service: Annotated[AuthService, Depends(deps.get_auth_service)],
) -> LoginResponse:
    """
    Email/password login.

    Returns:
    - access_token
    - refresh_token
    - user info
    """
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    return auth_service.login(
        payload,
        ip_address=ip_address,
        user_agent=user_agent,
    )


@router.post(
    "/login/phone",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login_with_phone(
    payload: PhoneLoginRequest,
    request: Request,
    auth_service: Annotated[AuthService, Depends(deps.get_auth_service)],
) -> LoginResponse:
    """
    Phone/password login.
    """
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    return auth_service.login_with_phone(
        payload,
        ip_address=ip_address,
        user_agent=user_agent,
    )