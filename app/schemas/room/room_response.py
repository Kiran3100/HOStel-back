"""
Room response schemas
"""
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import RoomType, RoomStatus


class RoomResponse(BaseResponseSchema):
    """Room response schema"""
    hostel_id: UUID
    room_number: str
    floor_number: Optional[int]
    wing: Optional[str]
    room_type: RoomType
    total_beds: int
    occupied_beds: int
    available_beds: int
    price_monthly: Decimal
    is_ac: bool
    has_attached_bathroom: bool
    status: RoomStatus
    is_available_for_booking: bool


class RoomDetail(BaseResponseSchema):
    """Detailed room information"""
    hostel_id: UUID
    hostel_name: str
    room_number: str
    floor_number: Optional[int]
    wing: Optional[str]
    
    # Type and capacity
    room_type: RoomType
    total_beds: int
    occupied_beds: int
    available_beds: int
    
    # Pricing
    price_monthly: Decimal
    price_quarterly: Optional[Decimal]
    price_half_yearly: Optional[Decimal]
    price_yearly: Optional[Decimal]
    
    # Specifications
    room_size_sqft: Optional[int]
    is_ac: bool
    has_attached_bathroom: bool
    has_balcony: bool
    has_wifi: bool
    
    # Amenities
    amenities: List[str]
    furnishing: List[str]
    
    # Status
    status: RoomStatus
    is_available_for_booking: bool
    is_under_maintenance: bool
    maintenance_start_date: Optional[date]
    maintenance_end_date: Optional[date]
    
    # Media
    room_images: List[str]
    
    # Beds detail
    beds: List["BedDetail"] = Field(default_factory=list)


class BedDetail(BaseSchema):
    """Bed detail in room"""
    id: UUID
    bed_number: str
    is_occupied: bool
    status: str
    current_student_id: Optional[UUID]
    current_student_name: Optional[str]
    occupied_from: Optional[date]


class RoomListItem(BaseSchema):
    """Room list item"""
    id: UUID
    room_number: str
    floor_number: Optional[int]
    wing: Optional[str]
    room_type: RoomType
    total_beds: int
    available_beds: int
    price_monthly: Decimal
    is_ac: bool
    status: RoomStatus
    is_available_for_booking: bool


class RoomWithBeds(BaseResponseSchema):
    """Room with bed information"""
    hostel_id: UUID
    room_number: str
    room_type: RoomType
    total_beds: int
    occupied_beds: int
    available_beds: int
    beds: List["BedInfo"]


class BedInfo(BaseSchema):
    """Bed information"""
    id: UUID
    bed_number: str
    is_occupied: bool
    status: str
    student_name: Optional[str] = None


class RoomOccupancyStats(BaseSchema):
    """Room occupancy statistics"""
    room_id: UUID
    room_number: str
    total_beds: int
    occupied_beds: int
    available_beds: int
    occupancy_percentage: Decimal
    current_revenue: Decimal
    potential_revenue: Decimal