# app/api/__init__.py
from __future__ import annotations

"""
Top-level API package.

This module primarily exists to expose convenient imports for the
versioned API routers.

Typical usage from outside:

    from app.api.v1 import api_router as api_v1_router
"""

from fastapi import APIRouter

# Re-export the v1 API router for convenience
from app.api.v1 import api_router as api_v1_router  # noqa: F401

# If you ever add more versions (v2, etc.), expose them here as well.

__all__ = [
    "APIRouter",
    "api_v1_router",
]