from __future__ import annotations

from fastapi import APIRouter

from . import dashboard
from . import hostels
from . import assignments
from . import permissions
from . import overrides
from . import multi_hostel

router = APIRouter(prefix="/admin")

router.include_router(dashboard.router, tags=["Admin - Dashboard"])
router.include_router(hostels.router, tags=["Admin - Hostels"])
router.include_router(assignments.router, tags=["Admin - Assignments"])
router.include_router(permissions.router, tags=["Admin - Permissions"])
router.include_router(overrides.router, tags=["Admin - Overrides"])
router.include_router(multi_hostel.router, tags=["Admin - Multi-Hostel"])

__all__ = ["router"]