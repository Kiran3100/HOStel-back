"""
Booking request schemas
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import EmailStr, Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.common.enums import RoomType


class GuestInformation(BaseSchema):
    """Guest information for booking"""
    guest_name: str = Field(..., min_length=2, max_length=255, description="Full name")
    guest_email: EmailStr = Field(..., description="Email address")
    guest_phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$', description="Phone number")
    
    # ID proof (optional at booking, required at check-in)
    guest_id_proof_type: Optional[str] = Field(
        None,
        pattern="^(aadhaar|passport|driving_license|voter_id|pan_card)$"
    )
    guest_id_proof_number: Optional[str] = Field(None, max_length=50)
    
    # Emergency contact
    emergency_contact_name: Optional[str] = Field(None, max_length=255)
    emergency_contact_phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{9,14}$')
    emergency_contact_relation: Optional[str] = Field(None, max_length=50)
    
    # Institutional/employment details
    institution_or_company: Optional[str] = Field(None, max_length=255)
    designation_or_course: Optional[str] = Field(None, max_length=255)


class BookingRequest(BaseCreateSchema):
    """Complete booking request"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    
    # Booking details
    room_type_requested: RoomType = Field(..., description="Desired room type")
    preferred_check_in_date: date = Field(..., description="Desired check-in date")
    stay_duration_months: int = Field(..., ge=1, le=24, description="Stay duration (1-24 months)")
    
    # Guest information
    guest_info: GuestInformation = Field(..., description="Guest details")
    
    # Special requests
    special_requests: Optional[str] = Field(None, max_length=1000)
    dietary_preferences: Optional[str] = Field(None, max_length=255)
    has_vehicle: bool = Field(False)
    vehicle_details: Optional[str] = Field(None, max_length=255)
    
    # Referral
    referral_code: Optional[str] = Field(None, max_length=50)
    
    @field_validator('preferred_check_in_date')
    @classmethod
    def validate_checkin_date(cls, v: date) -> date:
        """Validate check-in date is in future"""
        from datetime import date as date_type
        if v < date_type.today():
            raise ValueError('Check-in date must be in the future')
        return v


class BookingInquiry(BaseCreateSchema):
    """Simple inquiry (without full booking)"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    
    # Contact info
    visitor_name: str = Field(..., min_length=2, max_length=255)
    visitor_email: EmailStr = Field(...)
    visitor_phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$')
    
    # Interest details
    room_type_interest: Optional[RoomType] = None
    preferred_check_in_date: Optional[date] = None
    message: Optional[str] = Field(None, max_length=1000)


class QuickBookingRequest(BaseCreateSchema):
    """Quick booking (minimal information)"""
    hostel_id: UUID
    room_type_requested: RoomType
    check_in_date: date
    duration_months: int = Field(..., ge=1, le=24)
    
    # Minimal guest info (rest can be added later)
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$')