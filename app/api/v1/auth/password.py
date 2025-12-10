# api/v1/auth/password.py
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from api import deps
from app.schemas.auth.password import (
    PasswordChangeRequest,
    PasswordChangeResponse,
    PasswordStrengthCheck,
    PasswordStrengthResponse,
)
from app.services.auth import PasswordService

router = APIRouter()


@router.post(
    "/password/change",
    response_model=PasswordChangeResponse,
    status_code=status.HTTP_200_OK,
)
async def change_password(
    payload: PasswordChangeRequest,
    request: Request,
    password_service: Annotated[PasswordService, Depends(deps.get_password_service)],
    current_user=Depends(deps.get_current_user),
) -> PasswordChangeResponse:
    """
    Change password for the currently authenticated user.
    """
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    return password_service.change_password(
        user_id=current_user.id,
        data=payload,
        ip_address=ip_address,
        user_agent=user_agent,
    )


@router.post(
    "/password/strength",
    response_model=PasswordStrengthResponse,
    status_code=status.HTTP_200_OK,
)
async def evaluate_password_strength(
    payload: PasswordStrengthCheck,
    password_service: Annotated[PasswordService, Depends(deps.get_password_service)],
) -> PasswordStrengthResponse:
    """
    Simple password strength evaluation helper.
    """
    return password_service.evaluate_strength(payload)