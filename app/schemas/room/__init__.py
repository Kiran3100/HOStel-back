"""
Room schemas package
"""
from app.schemas.room.room_base import (
    RoomBase,
    RoomCreate,
    RoomUpdate,
    BulkRoomCreate
)
from app.schemas.room.room_response import (
    RoomResponse,
    RoomDetail,
    RoomListItem,
    RoomWithBeds
)
from app.schemas.room.bed_base import (
    BedBase,
    BedCreate,
    BedUpdate,
    BulkBedCreate
)
from app.schemas.room.bed_response import (
    BedResponse,
    BedAvailability,
    BedAssignment
)
from app.schemas.room.room_availability import (
    RoomAvailabilityRequest,
    AvailabilityResponse,
    AvailabilityCalendar
)

__all__ = [
    # Room base
    "RoomBase",
    "RoomCreate",
    "RoomUpdate",
    "BulkRoomCreate",
    
    # Room response
    "RoomResponse",
    "RoomDetail",
    "RoomListItem",
    "RoomWithBeds",
    
    # Bed base
    "BedBase",
    "BedCreate",
    "BedUpdate",
    "BulkBedCreate",
    
    # Bed response
    "BedResponse",
    "BedAvailability",
    "BedAssignment",
    
    # Availability
    "RoomAvailabilityRequest",
    "AvailabilityResponse",
    "AvailabilityCalendar",
]