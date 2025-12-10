# api/v1/auth/register.py
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from api import deps
from app.schemas.auth.register import (
    RegisterRequest,
    RegisterResponse,
)
from app.services.auth import RegistrationService

router = APIRouter()


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_visitor(
    payload: RegisterRequest,
    registration_service: Annotated[RegistrationService, Depends(deps.get_registration_service)],
) -> RegisterResponse:
    """
    Public visitor registration.

    Only VISITOR role is allowed here; other roles must be created by admins.
    """
    return registration_service.register(payload)