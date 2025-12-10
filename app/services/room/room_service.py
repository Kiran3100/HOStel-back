# app/services/room/room_service.py
from __future__ import annotations

from typing import Callable, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.core import RoomRepository
from app.schemas.common.pagination import PaginationParams, PaginatedResponse
from app.schemas.common.enums import RoomStatus
from app.schemas.room import (
    RoomCreate,
    RoomUpdate,
    RoomResponse,
    RoomDetail,
    RoomListItem,
    RoomPricingUpdate,
    RoomStatusUpdate,
)
from app.services.common import UnitOfWork, mapping, pagination, errors


class RoomService:
    """
    Room service:

    - Create/update rooms
    - Retrieve single room (detail)
    - List rooms per hostel
    - Update pricing and status
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    def _get_room_repo(self, uow: UnitOfWork) -> RoomRepository:
        return uow.get_repo(RoomRepository)

    # ------------------------------------------------------------------ #
    # Read
    # ------------------------------------------------------------------ #
    def get_room(self, room_id: UUID) -> RoomDetail:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_room_repo(uow)
            room = repo.get(room_id)
            if room is None:
                raise errors.NotFoundError(f"Room {room_id} not found")
            return mapping.to_schema(room, RoomDetail)

    def list_rooms_for_hostel(
        self,
        hostel_id: UUID,
        params: PaginationParams,
        *,
        only_available: bool = False,
    ) -> PaginatedResponse[RoomListItem]:
        """
        List rooms for a specific hostel.
        """
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_room_repo(uow)
            # Note: RoomRepository.list_for_hostel uses string(hostel_id)
            all_rooms = repo.list_for_hostel(
                hostel_id=hostel_id,
                only_available=only_available,
                room_type=None,
            )

            # Manual pagination in memory since RoomRepository returns full list
            total = len(all_rooms)
            start = params.offset
            end = start + params.limit
            page_items = all_rooms[start:end]

            return pagination.paginate(
                items=page_items,
                total_items=total,
                params=params,
                mapper=lambda r: mapping.to_schema(r, RoomListItem),
            )

    # ------------------------------------------------------------------ #
    # Create / update
    # ------------------------------------------------------------------ #
    def create_room(self, data: RoomCreate) -> RoomDetail:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_room_repo(uow)
            room = repo.create(data.model_dump())
            uow.commit()
            return mapping.to_schema(room, RoomDetail)

    def update_room(self, room_id: UUID, data: RoomUpdate) -> RoomDetail:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_room_repo(uow)
            room = repo.get(room_id)
            if room is None:
                raise errors.NotFoundError(f"Room {room_id} not found")

            mapping.update_model_from_schema(room, data, exclude_fields=["id"])
            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return mapping.to_schema(room, RoomDetail)

    # ------------------------------------------------------------------ #
    # Pricing & status
    # ------------------------------------------------------------------ #
    def update_pricing(self, room_id: UUID, data: RoomPricingUpdate) -> RoomDetail:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_room_repo(uow)
            room = repo.get(room_id)
            if room is None:
                raise errors.NotFoundError(f"Room {room_id} not found")

            mapping.update_model_from_schema(room, data, exclude_fields=["id"])
            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return mapping.to_schema(room, RoomDetail)

    def update_status(self, room_id: UUID, data: RoomStatusUpdate) -> RoomResponse:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_room_repo(uow)
            room = repo.get(room_id)
            if room is None:
                raise errors.NotFoundError(f"Room {room_id} not found")

            room.status = data.status  # type: ignore[attr-defined]
            room.is_available_for_booking = data.is_available_for_booking  # type: ignore[attr-defined]
            room.is_under_maintenance = data.is_under_maintenance  # type: ignore[attr-defined]
            # Maintenance notes currently not stored on Room model; consider
            # adding a column if you want to persist them.
            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return mapping.to_schema(room, RoomResponse)