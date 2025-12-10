"""
Booking calendar schemas
"""
from datetime import date, datetime
from typing import List, Dict, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.enums import BookingStatus


class CalendarView(BaseSchema):
    """Calendar view of bookings"""
    hostel_id: UUID
    month: str = Field(..., description="Month in YYYY-MM format")
    
    # Calendar data
    days: Dict[str, "DayBookings"] = Field(..., description="Bookings by date")
    
    # Summary
    total_check_ins: int
    total_check_outs: int
    peak_occupancy_date: Optional[date]
    
    # Room availability summary
    available_rooms_by_date: Dict[str, int]


class DayBookings(BaseSchema):
    """Bookings for a specific day"""
    date: date
    
    check_ins: List["BookingEvent"] = Field(default_factory=list)
    check_outs: List["BookingEvent"] = Field(default_factory=list)
    pending_bookings: List["BookingEvent"] = Field(default_factory=list)
    
    available_beds: int
    total_beds: int


class BookingEvent(BaseSchema):
    """Booking event for calendar"""
    booking_id: UUID
    booking_reference: str
    guest_name: str
    room_number: Optional[str]
    room_type: str
    status: BookingStatus
    
    # For check-in events
    is_check_in: bool = Field(False)
    # For check-out events  
    is_check_out: bool = Field(False)


class CalendarEvent(BaseSchema):
    """Generic calendar event"""
    event_id: UUID
    event_type: str = Field(..., pattern="^(check_in|check_out|booking_request|maintenance)$")
    title: str
    start_date: date
    end_date: Optional[date]
    
    # Related entities
    booking_id: Optional[UUID] = None
    room_id: Optional[UUID] = None
    
    # Display
    color: str = Field(..., description="Color code for event")
    is_all_day: bool = Field(True)


class AvailabilityCalendar(BaseSchema):
    """Room availability calendar"""
    hostel_id: UUID
    room_id: Optional[UUID] = Field(None, description="Specific room or all rooms")
    month: str = Field(..., description="YYYY-MM")
    
    availability: Dict[str, "DayAvailability"]


class DayAvailability(BaseSchema):
    """Availability for a specific day"""
    date: date
    total_beds: int
    available_beds: int
    booked_beds: int
    is_fully_booked: bool
    
    # Bookings for this day
    active_bookings: List[UUID] = Field(default_factory=list)