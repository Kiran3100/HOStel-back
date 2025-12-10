"""
Booking base schemas
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import BookingStatus, RoomType, BookingSource


class BookingBase(BaseSchema):
    """Base booking schema"""
    visitor_id: UUID = Field(..., description="Visitor/guest making booking")
    hostel_id: UUID = Field(..., description="Hostel being booked")
    
    # Booking details
    room_type_requested: RoomType = Field(..., description="Requested room type")
    preferred_check_in_date: date = Field(..., description="Preferred check-in date")
    stay_duration_months: int = Field(..., ge=1, le=24, description="Stay duration in months")
    
    # Pricing
    quoted_rent_monthly: Decimal = Field(..., ge=0, description="Quoted monthly rent")
    total_amount: Decimal = Field(..., ge=0, description="Total amount")
    security_deposit: Decimal = Field(Decimal("0.00"), ge=0, description="Security deposit")
    advance_amount: Decimal = Field(Decimal("0.00"), ge=0, description="Advance payment amount")
    
    # Special requests
    special_requests: Optional[str] = Field(None, max_length=1000, description="Special requests")
    dietary_preferences: Optional[str] = Field(None, max_length=255, description="Dietary preferences")
    has_vehicle: bool = Field(False, description="Has vehicle")
    vehicle_details: Optional[str] = Field(None, max_length=255, description="Vehicle details")
    
    # Source
    source: BookingSource = Field(BookingSource.WEBSITE, description="Booking source")
    referral_code: Optional[str] = Field(None, max_length=50, description="Referral code used")
    
    @field_validator('total_amount')
    @classmethod
    def validate_total_amount(cls, v: Decimal, info) -> Decimal:
        """Validate total amount calculation"""
        if 'quoted_rent_monthly' in info.data and 'stay_duration_months' in info.data:
            expected = info.data['quoted_rent_monthly'] * info.data['stay_duration_months']
            if abs(v - expected) > Decimal('0.01'):  # Allow small floating point differences
                raise ValueError(f'Total amount should be approximately {expected}')
        return v


class BookingCreate(BookingBase, BaseCreateSchema):
    """Create booking schema"""
    # Guest information embedded
    guest_name: str = Field(..., min_length=2, max_length=255)
    guest_email: str = Field(...)
    guest_phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$')
    
    # Optional ID proof
    guest_id_proof_type: Optional[str] = None
    guest_id_proof_number: Optional[str] = None
    
    # Emergency contact
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    
    # Institutional/employment
    institution_or_company: Optional[str] = None
    designation_or_course: Optional[str] = None


class BookingUpdate(BaseUpdateSchema):
    """Update booking schema"""
    room_type_requested: Optional[RoomType] = None
    preferred_check_in_date: Optional[date] = None
    stay_duration_months: Optional[int] = Field(None, ge=1, le=24)
    
    special_requests: Optional[str] = None
    dietary_preferences: Optional[str] = None
    has_vehicle: Optional[bool] = None
    vehicle_details: Optional[str] = None
    
    # Status updates (admin only)
    booking_status: Optional[BookingStatus] = None