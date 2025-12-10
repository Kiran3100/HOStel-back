"""
Room availability schemas
"""
from datetime import date
from typing import List, Optional, Dict
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import RoomType


class RoomAvailabilityRequest(BaseCreateSchema):
    """Check room availability"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    check_in_date: date = Field(..., description="Desired check-in date")
    duration_months: int = Field(..., ge=1, le=24, description="Stay duration")
    room_type: Optional[RoomType] = Field(None, description="Preferred room type")


class AvailabilityResponse(BaseSchema):
    """Room availability response"""
    hostel_id: UUID
    check_in_date: date
    check_out_date: date
    available_rooms: List["AvailableRoom"]
    total_available_beds: int
    has_availability: bool


class AvailableRoom(BaseSchema):
    """Available room details"""
    room_id: UUID
    room_number: str
    room_type: RoomType
    floor_number: Optional[int]
    available_beds: int
    total_beds: int
    price_monthly: Decimal
    is_ac: bool
    has_attached_bathroom: bool
    amenities: List[str]
    room_images: List[str]


class AvailabilityCalendar(BaseSchema):
    """Availability calendar for a room"""
    room_id: UUID
    room_number: str
    month: str = Field(..., description="Month in YYYY-MM format")
    availability: Dict[str, "DayAvailability"] = Field(
        ...,
        description="Availability by date (date string as key)"
    )


class DayAvailability(BaseSchema):
    """Availability for a specific day"""
    date: date
    available_beds: int
    total_beds: int
    is_available: bool
    bookings: List["BookingInfo"] = Field(default_factory=list)


class BookingInfo(BaseSchema):
    """Booking information for calendar"""
    booking_id: UUID
    student_name: str
    check_in_date: date
    check_out_date: date