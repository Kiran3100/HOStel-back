"""
Booking response schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import BookingStatus, RoomType, BookingSource


class BookingResponse(BaseResponseSchema):
    """Booking response schema"""
    booking_reference: str
    visitor_id: UUID
    hostel_id: UUID
    hostel_name: str
    
    room_type_requested: RoomType
    preferred_check_in_date: date
    stay_duration_months: int
    expected_check_out_date: date
    
    # Guest info
    guest_name: str
    guest_email: str
    guest_phone: str
    
    # Pricing
    quoted_rent_monthly: Decimal
    total_amount: Decimal
    security_deposit: Decimal
    advance_amount: Decimal
    advance_paid: bool
    
    # Status
    booking_status: BookingStatus
    
    # Dates
    booking_date: datetime
    expires_at: Optional[datetime]


class BookingDetail(BaseResponseSchema):
    """Detailed booking information"""
    booking_reference: str
    visitor_id: UUID
    visitor_name: str
    
    hostel_id: UUID
    hostel_name: str
    hostel_city: str
    hostel_address: str
    hostel_phone: str
    
    # Requested details
    room_type_requested: RoomType
    preferred_check_in_date: date
    stay_duration_months: int
    expected_check_out_date: date
    
    # Assignment (if approved)
    room_id: Optional[UUID]
    room_number: Optional[str]
    bed_id: Optional[UUID]
    bed_number: Optional[str]
    
    # Guest information
    guest_name: str
    guest_email: str
    guest_phone: str
    guest_id_proof_type: Optional[str]
    guest_id_proof_number: Optional[str]
    
    # Emergency contact
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    emergency_contact_relation: Optional[str]
    
    # Institutional/employment
    institution_or_company: Optional[str]
    designation_or_course: Optional[str]
    
    # Special requests
    special_requests: Optional[str]
    dietary_preferences: Optional[str]
    has_vehicle: bool
    vehicle_details: Optional[str]
    
    # Pricing
    quoted_rent_monthly: Decimal
    total_amount: Decimal
    security_deposit: Decimal
    advance_amount: Decimal
    advance_paid: bool
    advance_payment_id: Optional[UUID]
    
    # Status workflow
    booking_status: BookingStatus
    approved_by: Optional[UUID]
    approved_by_name: Optional[str]
    approved_at: Optional[datetime]
    rejected_by: Optional[UUID]
    rejected_at: Optional[datetime]
    rejection_reason: Optional[str]
    
    # Cancellation
    cancelled_by: Optional[UUID]
    cancelled_at: Optional[datetime]
    cancellation_reason: Optional[str]
    
    # Conversion
    converted_to_student: bool
    student_profile_id: Optional[UUID]
    conversion_date: Optional[date]
    
    # Source
    source: BookingSource
    referral_code: Optional[str]
    
    # Timestamps
    booking_date: datetime
    expires_at: Optional[datetime]


class BookingListItem(BaseSchema):
    """Booking list item"""
    id: UUID
    booking_reference: str
    guest_name: str
    guest_phone: str
    
    hostel_name: str
    room_type_requested: str
    
    preferred_check_in_date: date
    stay_duration_months: int
    
    total_amount: Decimal
    advance_paid: bool
    
    booking_status: BookingStatus
    booking_date: datetime
    
    # Quick indicators
    is_urgent: bool = Field(..., description="Expiring soon")
    days_until_checkin: Optional[int]


class BookingConfirmation(BaseSchema):
    """Booking confirmation response"""
    booking_id: UUID
    booking_reference: str
    
    hostel_name: str
    room_type: str
    check_in_date: date
    
    total_amount: Decimal
    advance_amount: Decimal
    balance_amount: Decimal
    
    confirmation_message: str
    next_steps: list[str]
    
    # Contact
    hostel_contact_phone: str
    hostel_contact_email: Optional[str]