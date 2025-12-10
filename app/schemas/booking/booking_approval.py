"""
Booking approval schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema


class BookingApprovalRequest(BaseCreateSchema):
    """Approve booking request"""
    booking_id: UUID = Field(..., description="Booking ID to approve")
    
    # Room assignment
    room_id: UUID = Field(..., description="Assigned room")
    bed_id: UUID = Field(..., description="Assigned bed")
    
    # Confirm or adjust dates
    approved_check_in_date: date = Field(..., description="Approved check-in date")
    
    # Confirm or adjust pricing
    final_rent_monthly: Decimal = Field(..., ge=0, description="Final monthly rent")
    final_security_deposit: Decimal = Field(..., ge=0, description="Final security deposit")
    
    # Additional charges
    processing_fee: Decimal = Field(Decimal("0.00"), ge=0, description="One-time processing fee")
    
    # Notes
    admin_notes: Optional[str] = Field(None, max_length=500, description="Internal notes")
    message_to_guest: Optional[str] = Field(None, max_length=1000, description="Message to guest")
    
    # Payment requirement
    advance_payment_required: bool = Field(True, description="Require advance payment")
    advance_payment_percentage: Decimal = Field(
        Decimal("20.00"),
        ge=0,
        le=100,
        description="Advance payment %"
    )


class ApprovalResponse(BaseSchema):
    """Booking approval response"""
    booking_id: UUID
    booking_reference: str
    
    status: str = Field("approved", description="New status")
    
    # Assignment details
    room_number: str
    bed_number: str
    
    # Final amounts
    monthly_rent: Decimal
    security_deposit: Decimal
    advance_amount: Decimal
    total_amount: Decimal
    
    # Dates
    approved_at: datetime
    check_in_date: date
    
    # Next steps
    payment_pending: bool
    payment_deadline: Optional[datetime]
    
    message: str


class RejectionRequest(BaseCreateSchema):
    """Reject booking request"""
    booking_id: UUID = Field(..., description="Booking ID to reject")
    rejection_reason: str = Field(..., min_length=10, max_length=500, description="Reason for rejection")
    
    # Suggest alternatives
    suggest_alternative_dates: bool = Field(False)
    alternative_check_in_dates: Optional[list[date]] = Field(None, max_items=3)
    
    suggest_alternative_room_types: bool = Field(False)
    alternative_room_types: Optional[list[str]] = None
    
    # Message to guest
    message_to_guest: Optional[str] = Field(None, max_length=1000)


class BulkApprovalRequest(BaseCreateSchema):
    """Approve multiple bookings"""
    booking_ids: list[UUID] = Field(..., min_items=1, description="Booking IDs to approve")
    
    # Common settings
    auto_assign_rooms: bool = Field(True, description="Auto-assign available rooms")
    send_notifications: bool = Field(True, description="Send approval notifications")


class ApprovalSettings(BaseSchema):
    """Hostel booking approval settings"""
    hostel_id: UUID
    
    auto_approve_enabled: bool = Field(False, description="Auto-approve bookings")
    auto_approve_conditions: dict = Field(
        default_factory=dict,
        description="Conditions for auto-approval"
    )
    
    approval_expiry_hours: int = Field(48, ge=1, le=168, description="Hours to respond to booking")
    
    require_advance_payment: bool = Field(True)
    advance_payment_percentage: Decimal = Field(Decimal("20.00"), ge=0, le=100)