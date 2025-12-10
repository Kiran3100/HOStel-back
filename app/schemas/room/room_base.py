"""
Room base schemas
"""
from decimal import Decimal
from typing import List, Optional
from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import RoomType, RoomStatus


class RoomBase(BaseSchema):
    """Base room schema"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    room_number: str = Field(..., min_length=1, max_length=50, description="Room number/identifier")
    floor_number: Optional[int] = Field(None, ge=0, le=50, description="Floor number")
    wing: Optional[str] = Field(None, max_length=50, description="Wing/Block (A, B, North, etc.)")
    
    # Type and capacity
    room_type: RoomType = Field(..., description="Room type")
    total_beds: int = Field(..., ge=1, le=20, description="Total beds in room")
    
    # Pricing
    price_monthly: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2, description="Monthly rent")
    price_quarterly: Optional[Decimal] = Field(None, ge=0, max_digits=10, decimal_places=2)
    price_half_yearly: Optional[Decimal] = Field(None, ge=0, max_digits=10, decimal_places=2)
    price_yearly: Optional[Decimal] = Field(None, ge=0, max_digits=10, decimal_places=2)
    
    # Specifications
    room_size_sqft: Optional[int] = Field(None, ge=50, le=1000, description="Room size in sq ft")
    is_ac: bool = Field(False, description="Air conditioned")
    has_attached_bathroom: bool = Field(False, description="Attached bathroom")
    has_balcony: bool = Field(False, description="Has balcony")
    has_wifi: bool = Field(True, description="WiFi available")
    
    # Amenities
    amenities: List[str] = Field(default_factory=list, description="Room amenities")
    furnishing: List[str] = Field(default_factory=list, description="Furniture items")
    
    # Availability
    is_available_for_booking: bool = Field(True, description="Available for online booking")
    is_under_maintenance: bool = Field(False, description="Under maintenance")
    
    # Media
    room_images: List[str] = Field(default_factory=list, description="Room image URLs")


class RoomCreate(RoomBase, BaseCreateSchema):
    """Create room schema"""
    pass


class RoomUpdate(BaseUpdateSchema):
    """Update room schema"""
    room_number: Optional[str] = Field(None, min_length=1, max_length=50)
    floor_number: Optional[int] = Field(None, ge=0, le=50)
    wing: Optional[str] = None
    room_type: Optional[RoomType] = None
    
    # Pricing updates
    price_monthly: Optional[Decimal] = Field(None, ge=0)
    price_quarterly: Optional[Decimal] = Field(None, ge=0)
    price_half_yearly: Optional[Decimal] = Field(None, ge=0)
    price_yearly: Optional[Decimal] = Field(None, ge=0)
    
    # Features
    is_ac: Optional[bool] = None
    has_attached_bathroom: Optional[bool] = None
    has_balcony: Optional[bool] = None
    has_wifi: Optional[bool] = None
    
    # Lists
    amenities: Optional[List[str]] = None
    furnishing: Optional[List[str]] = None
    room_images: Optional[List[str]] = None
    
    # Status
    is_available_for_booking: Optional[bool] = None
    is_under_maintenance: Optional[bool] = None
    status: Optional[RoomStatus] = None


class BulkRoomCreate(BaseCreateSchema):
    """Bulk create rooms"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    rooms: List[RoomCreate] = Field(..., min_items=1, max_items=100, description="List of rooms to create")


class RoomPricingUpdate(BaseUpdateSchema):
    """Update room pricing"""
    price_monthly: Decimal = Field(..., ge=0, description="Monthly rent")
    price_quarterly: Optional[Decimal] = Field(None, ge=0)
    price_half_yearly: Optional[Decimal] = Field(None, ge=0)
    price_yearly: Optional[Decimal] = Field(None, ge=0)


class RoomStatusUpdate(BaseUpdateSchema):
    """Update room status"""
    status: RoomStatus = Field(..., description="Room status")
    is_available_for_booking: bool = Field(..., description="Booking availability")
    is_under_maintenance: bool = Field(False, description="Maintenance flag")
    maintenance_notes: Optional[str] = Field(None, description="Maintenance details")