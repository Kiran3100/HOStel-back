"""
Booking filter and search schemas
"""
from datetime import date
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import BookingStatus, BookingSource, RoomType


class BookingFilterParams(BaseFilterSchema):
    """Booking filter parameters"""
    # Text search
    search: Optional[str] = Field(None, description="Search in reference, guest name, email, phone")
    
    # Hostel filter
    hostel_id: Optional[UUID] = None
    hostel_ids: Optional[List[UUID]] = None
    
    # Status filter
    status: Optional[BookingStatus] = None
    statuses: Optional[List[BookingStatus]] = None
    
    # Date filters
    booking_date_from: Optional[date] = None
    booking_date_to: Optional[date] = None
    check_in_date_from: Optional[date] = None
    check_in_date_to: Optional[date] = None
    
    # Room type
    room_type: Optional[RoomType] = None
    
    # Source
    source: Optional[BookingSource] = None
    
    # Payment status
    advance_paid: Optional[bool] = None
    
    # Conversion status
    converted_to_student: Optional[bool] = None
    
    # Expiry
    expiring_soon: Optional[bool] = Field(None, description="Bookings expiring in next 24 hours")
    expired: Optional[bool] = None


class BookingSearchRequest(BaseFilterSchema):
    """Booking search request"""
    query: str = Field(..., min_length=1, description="Search query")
    hostel_id: Optional[UUID] = None
    
    # Search fields
    search_in_reference: bool = Field(True)
    search_in_guest_name: bool = Field(True)
    search_in_email: bool = Field(True)
    search_in_phone: bool = Field(True)
    
    # Status filter
    status: Optional[BookingStatus] = None
    
    # Pagination
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class BookingSortOptions(BaseFilterSchema):
    """Booking sorting options"""
    sort_by: str = Field(
        "booking_date",
        pattern="^(booking_date|check_in_date|guest_name|status|total_amount)$"
    )
    sort_order: str = Field("desc", pattern="^(asc|desc)$")


class BookingExportRequest(BaseFilterSchema):
    """Export bookings"""
    hostel_id: Optional[UUID] = None
    filters: Optional[BookingFilterParams] = None
    
    format: str = Field("csv", pattern="^(csv|excel|pdf)$")
    
    # Fields to include
    include_guest_details: bool = Field(True)
    include_payment_details: bool = Field(True)
    include_assignment_details: bool = Field(True)


class BookingAnalyticsRequest(BaseFilterSchema):
    """Booking analytics request"""
    hostel_id: Optional[UUID] = None
    date_from: date
    date_to: date
    
    group_by: str = Field("day", pattern="^(day|week|month)$")