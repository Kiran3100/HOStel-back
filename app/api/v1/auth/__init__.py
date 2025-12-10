# api/v1/auth/__init__.py
from __future__ import annotations

from fastapi import APIRouter

from . import login, register, token, password, otp, social

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(login.router)
router.include_router(register.router)
router.include_router(token.router)
router.include_router(password.router)
router.include_router(otp.router)
router.include_router(social.router)

__all__ = ["router"]