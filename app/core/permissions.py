# app/core/permissions.py
from __future__ import annotations

"""
Core permission helpers.

These re-export the RBAC helpers from app.services.common.permissions
so they can be imported from a core location.
"""

from app.services.common.permissions import (
    Principal,
    PermissionDenied,
    role_in,
    has_permission,
    require_permission,
)

__all__ = [
    "Principal",
    "PermissionDenied",
    "role_in",
    "has_permission",
    "require_permission",
]