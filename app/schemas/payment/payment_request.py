"""
Payment request schemas
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.common.enums import PaymentType, PaymentMethod


class PaymentRequest(BaseCreateSchema):
    """Online payment request"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    student_id: Optional[UUID] = Field(None, description="Student ID (for recurring fees)")
    booking_id: Optional[UUID] = Field(None, description="Booking ID (for booking payment)")
    
    payment_type: PaymentType = Field(..., description="Type of payment")
    amount: Decimal = Field(..., ge=0, description="Amount to pay")
    
    # For recurring fees
    payment_period_start: Optional[date] = None
    payment_period_end: Optional[date] = None
    
    # Payment method
    payment_method: PaymentMethod = Field(PaymentMethod.PAYMENT_GATEWAY, description="Payment method")
    payment_gateway: str = Field("razorpay", pattern="^(razorpay|stripe|paytm)$")
    
    # Return URLs
    success_url: Optional[str] = Field(None, description="URL to redirect on success")
    failure_url: Optional[str] = Field(None, description="URL to redirect on failure")
    cancel_url: Optional[str] = Field(None, description="URL if payment cancelled")


class PaymentInitiation(BaseSchema):
    """Payment initiation response"""
    payment_id: UUID
    payment_reference: str
    
    amount: Decimal
    currency: str
    
    # Gateway details
    gateway: str
    gateway_order_id: str
    gateway_key: str
    
    # Checkout info
    checkout_url: Optional[str] = None
    checkout_token: Optional[str] = None
    
    # For client-side integration
    gateway_options: dict = Field(..., description="Gateway-specific options")


class ManualPaymentRequest(BaseCreateSchema):
    """Manual payment recording (cash/cheque)"""
    hostel_id: UUID
    student_id: UUID
    
    payment_type: PaymentType
    amount: Decimal = Field(..., ge=0)
    
    payment_method: PaymentMethod = Field(..., pattern="^(cash|cheque|bank_transfer)$")
    
    # For cheque
    cheque_number: Optional[str] = None
    cheque_date: Optional[date] = None
    bank_name: Optional[str] = None
    
    # For bank transfer
    transaction_reference: Optional[str] = None
    transfer_date: Optional[date] = None
    
    # Period
    payment_period_start: Optional[date] = None
    payment_period_end: Optional[date] = None
    
    # Collection details
    collected_by: UUID = Field(..., description="Staff member who collected")
    collection_date: date = Field(..., description="Date of collection")
    
    notes: Optional[str] = Field(None, max_length=500)


class BulkPaymentRequest(BaseCreateSchema):
    """Record multiple payments"""
    hostel_id: UUID
    payments: List["SinglePaymentRecord"] = Field(..., min_items=1, max_items=100)
    
    collected_by: UUID
    collection_date: date


class SinglePaymentRecord(BaseSchema):
    """Single payment in bulk"""
    student_id: UUID
    payment_type: PaymentType
    amount: Decimal
    payment_method: PaymentMethod
    
    # Optional fields
    transaction_reference: Optional[str] = None
    notes: Optional[str] = None