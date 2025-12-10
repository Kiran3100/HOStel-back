"""
Payment base schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import PaymentType, PaymentMethod, PaymentStatus


class PaymentBase(BaseSchema):
    """Base payment schema"""
    payer_id: UUID = Field(..., description="User making payment")
    hostel_id: UUID = Field(..., description="Hostel receiving payment")
    student_id: Optional[UUID] = Field(None, description="Student profile (for recurring fees)")
    booking_id: Optional[UUID] = Field(None, description="Booking (for booking payments)")
    
    # Payment details
    payment_type: PaymentType = Field(..., description="Type of payment")
    amount: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2, description="Payment amount")
    currency: str = Field("INR", min_length=3, max_length=3, description="Currency code")
    
    # Period covered (for recurring fees)
    payment_period_start: Optional[date] = Field(None, description="Period start date")
    payment_period_end: Optional[date] = Field(None, description="Period end date")
    
    # Payment method
    payment_method: PaymentMethod = Field(..., description="Payment method")
    payment_gateway: Optional[str] = Field(None, description="Gateway used (razorpay/stripe/paytm)")
    
    # Due date (for scheduled payments)
    due_date: Optional[date] = Field(None, description="Payment due date")


class PaymentCreate(PaymentBase, BaseCreateSchema):
    """Create payment schema"""
    # Additional creation fields
    transaction_id: Optional[str] = Field(None, description="External transaction ID")
    collected_by: Optional[UUID] = Field(None, description="Staff who collected (for cash/cheque)")


class PaymentUpdate(BaseUpdateSchema):
    """Update payment schema"""
    payment_status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    
    # Receipt
    receipt_number: Optional[str] = None
    receipt_url: Optional[str] = None