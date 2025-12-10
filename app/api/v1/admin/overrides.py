from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from api.deps import get_uow
from app.core.exceptions import (
    ServiceError,
    NotFoundError,
    ValidationError,
    ConflictError,
)
from app.schemas.admin.admin_override import (
    AdminOverrideRequest,
    OverrideLog,
    OverrideSummary,
    SupervisorOverrideStats,
)
from app.services.common.unit_of_work import UnitOfWork
from app.services.admin import AdminOverrideService

router = APIRouter(prefix="/overrides")


def _map_service_error(exc: ServiceError) -> HTTPException:
    if isinstance(exc, NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, ValidationError):
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    if isinstance(exc, ConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post(
    "",
    response_model=OverrideLog,
    status_code=status.HTTP_201_CREATED,
    summary="Create an admin override",
)
async def create_admin_override(
    payload: AdminOverrideRequest,
    uow: UnitOfWork = Depends(get_uow),
) -> OverrideLog:
    """
    Record an admin override of a supervisor decision.

    Also expected to create generic audit entries internally.
    """
    service = AdminOverrideService(uow)
    try:
        return service.create_override(request=payload)
    except ServiceError as exc:
        raise _map_service_error(exc)


@router.get(
    "/entity/{entity_type}/{entity_id}",
    response_model=List[OverrideLog],
    summary="List overrides for a specific entity",
)
async def list_overrides_for_entity(
    entity_type: str = Path(..., description="Entity type (complaint, maintenance, leave, etc.)"),
    entity_id: UUID = Path(..., description="Entity ID"),
    uow: UnitOfWork = Depends(get_uow),
) -> List[OverrideLog]:
    """
    Fetch all overrides applied to a particular entity.
    """
    service = AdminOverrideService(uow)
    try:
        return service.list_overrides_for_entity(entity_type=entity_type, entity_id=entity_id)
    except ServiceError as exc:
        raise _map_service_error(exc)


@router.get(
    "/summary",
    response_model=OverrideSummary,
    summary="Get override summary for a period",
)
async def get_override_summary(
    hostel_id: Optional[UUID] = Query(None, description="Filter by hostel"),
    supervisor_id: Optional[UUID] = Query(None, description="Filter by supervisor"),
    start_date: Optional[date] = Query(None, description="Start date (inclusive)"),
    end_date: Optional[date] = Query(None, description="End date (inclusive)"),
    uow: UnitOfWork = Depends(get_uow),
) -> OverrideSummary:
    """
    Summarize overrides over a period, optionally filtered by hostel/supervisor.
    """
    service = AdminOverrideService(uow)
    try:
        return service.get_override_summary(
            hostel_id=hostel_id,
            supervisor_id=supervisor_id,
            start_date=start_date,
            end_date=end_date,
        )
    except ServiceError as exc:
        raise _map_service_error(exc)


@router.get(
    "/supervisors/{supervisor_id}/stats",
    response_model=SupervisorOverrideStats,
    summary="Get override stats for a supervisor",
)
async def get_supervisor_override_stats(
    supervisor_id: UUID = Path(..., description="Supervisor ID"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    uow: UnitOfWork = Depends(get_uow),
) -> SupervisorOverrideStats:
    """
    Supervisor-specific override statistics (counts, types, trends).
    """
    service = AdminOverrideService(uow)
    try:
        return service.get_supervisor_override_stats(
            supervisor_id=supervisor_id,
            start_date=start_date,
            end_date=end_date,
        )
    except ServiceError as exc:
        raise _map_service_error(exc)