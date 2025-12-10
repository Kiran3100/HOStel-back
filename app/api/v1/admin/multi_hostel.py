from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.deps import get_uow, get_current_active_user
from app.core.exceptions import (
    ServiceError,
    NotFoundError,
    ValidationError,
    ConflictError,
)
from app.models.core import User
from app.schemas.admin.multi_hostel_dashboard import MultiHostelDashboard
from app.services.common.unit_of_work import UnitOfWork
from app.services.admin import MultiHostelDashboardService

router = APIRouter(prefix="/multi-hostel")


def _map_service_error(exc: ServiceError) -> HTTPException:
    if isinstance(exc, NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, ValidationError):
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    if isinstance(exc, ConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get(
    "/dashboard",
    response_model=MultiHostelDashboard,
    summary="Get multi-hostel dashboard for an admin",
)
async def get_multi_hostel_dashboard(
    admin_id: Optional[UUID] = Query(
        None,
        description="Admin ID (optional; if omitted, resolved from current user)",
    ),
    current_user: User = Depends(get_current_active_user),
    uow: UnitOfWork = Depends(get_uow),
) -> MultiHostelDashboard:
    """
    Build a consolidated dashboard for an admin managing multiple hostels.

    If `admin_id` is not provided, it is derived from the current user's admin profile.
    """
    # Derive admin_id from current user if not explicitly provided
    if admin_id is None:
        admin_profile = getattr(current_user, "admin_profile", None)
        if admin_profile is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Current user is not an admin",
            )
        admin_id = admin_profile.id

    service = MultiHostelDashboardService(uow)
    try:
        return service.get_dashboard(admin_id=admin_id)
    except ServiceError as exc:
        raise _map_service_error(exc)