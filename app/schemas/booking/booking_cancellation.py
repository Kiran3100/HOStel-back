"""
Booking cancellation schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class CancellationRequest(BaseCreateSchema):
    """Request to cancel booking"""
    booking_id: UUID = Field(..., description="Booking ID to cancel")
    cancelled_by_role: str = Field(
        ...,
        pattern="^(visitor|admin|system)$",
        description="Who is cancelling"
    )
    
    cancellation_reason: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Reason for cancellation"
    )
    
    # Refund preference
    request_refund: bool = Field(True, description="Request refund of advance payment")
    
    # Additional details
    additional_comments: Optional[str] = Field(None, max_length=1000)


class CancellationResponse(BaseSchema):
    """Cancellation response"""
    booking_id: UUID
    booking_reference: str
    
    cancelled: bool
    cancelled_at: datetime
    
    # Refund information
    refund: "RefundCalculation"
    
    message: str
    confirmation_sent: bool


class RefundCalculation(BaseSchema):
    """Refund calculation details"""
    advance_paid: Decimal
    cancellation_charge: Decimal
    cancellation_charge_percentage: Decimal
    
    refundable_amount: Decimal
    refund_processing_time_days: int
    
    # Refund method
    refund_method: str = Field(..., description="How refund will be processed")
    
    # Breakdown
    breakdown: dict = Field(
        ...,
        description="Detailed refund breakdown"
    )


class CancellationPolicy(BaseSchema):
    """Hostel cancellation policy"""
    hostel_id: UUID
    
    # Charges based on timing
    cancellation_before_days: List["CancellationCharge"] = Field(
        ...,
        description="Cancellation charges based on days before check-in"
    )
    
    # Special conditions
    no_show_charge_percentage: Decimal = Field(
        Decimal("100.00"),
        description="Charge if guest doesn't show up"
    )
    
    refund_processing_days: int = Field(7, description="Days to process refund")
    
    policy_text: str = Field(..., description="Full policy text")


class CancellationCharge(BaseSchema):
    """Cancellation charge tier"""
    days_before_checkin: int = Field(..., description="Days before check-in")
    charge_percentage: Decimal = Field(..., ge=0, le=100, description="% of advance to charge")
    
    description: str


class BulkCancellation(BaseCreateSchema):
    """Cancel multiple bookings"""
    booking_ids: List[UUID] = Field(..., min_items=1)
    reason: str = Field(..., min_length=10)
    process_refunds: bool = Field(True)