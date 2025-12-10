"""
Payment response schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import PaymentType, PaymentMethod, PaymentStatus


class PaymentResponse(BaseResponseSchema):
    """Payment response schema"""
    payment_reference: str
    transaction_id: Optional[str]
    
    payer_id: UUID
    payer_name: str
    hostel_id: UUID
    hostel_name: str
    
    payment_type: PaymentType
    amount: Decimal
    currency: str
    
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    
    paid_at: Optional[datetime]
    due_date: Optional[date]
    is_overdue: bool
    
    receipt_number: Optional[str]
    receipt_url: Optional[str]


class PaymentDetail(BaseResponseSchema):
    """Detailed payment information"""
    payment_reference: str
    transaction_id: Optional[str]
    
    # Payer details
    payer_id: UUID
    payer_name: str
    payer_email: str
    payer_phone: str
    
    # Payee details
    hostel_id: UUID
    hostel_name: str
    
    # Related entities
    student_id: Optional[UUID]
    student_name: Optional[str]
    booking_id: Optional[UUID]
    booking_reference: Optional[str]
    
    # Payment details
    payment_type: PaymentType
    amount: Decimal
    currency: str
    
    # Period
    payment_period_start: Optional[date]
    payment_period_end: Optional[date]
    
    # Method
    payment_method: PaymentMethod
    payment_gateway: Optional[str]
    
    # Status
    payment_status: PaymentStatus
    paid_at: Optional[datetime]
    failed_at: Optional[datetime]
    failure_reason: Optional[str]
    
    # Gateway response
    gateway_response: Optional[dict]
    
    # Receipt
    receipt_number: Optional[str]
    receipt_url: Optional[str]
    receipt_generated_at: Optional[datetime]
    
    # Refund
    refund_amount: Decimal
    refund_status: str
    refunded_at: Optional[datetime]
    refund_transaction_id: Optional[str]
    refund_reason: Optional[str]
    
    # Collection
    collected_by: Optional[UUID]
    collected_by_name: Optional[str]
    collected_at: Optional[datetime]
    
    # Due date
    due_date: Optional[date]
    is_overdue: bool
    
    # Reminders
    reminder_sent_count: int
    last_reminder_sent_at: Optional[datetime]


class PaymentReceipt(BaseSchema):
    """Payment receipt"""
    receipt_number: str
    payment_reference: str
    
    # Payer
    payer_name: str
    payer_email: str
    payer_phone: str
    
    # Hostel
    hostel_name: str
    hostel_address: str
    hostel_phone: str
    
    # Payment details
    payment_type: str
    amount: Decimal
    amount_in_words: str
    currency: str
    
    payment_method: str
    transaction_id: Optional[str]
    
    # Period
    payment_for_period: Optional[str] = Field(None, description="e.g., 'January 2024'")
    
    # Dates
    payment_date: datetime
    due_date: Optional[date]
    
    # Receipt metadata
    receipt_generated_at: datetime
    receipt_url: str
    
    # Tax/GST details (if applicable)
    tax_details: Optional[dict] = None


class PaymentListItem(BaseSchema):
    """Payment list item"""
    id: UUID
    payment_reference: str
    payer_name: str
    hostel_name: str
    
    payment_type: str
    amount: Decimal
    
    payment_method: str
    payment_status: PaymentStatus
    
    paid_at: Optional[datetime]
    due_date: Optional[date]
    is_overdue: bool
    
    created_at: datetime


class PaymentSummary(BaseSchema):
    """Payment summary for student/hostel"""
    entity_id: UUID
    entity_type: str = Field(..., pattern="^(student|hostel)$")
    
    # Totals
    total_paid: Decimal
    total_pending: Decimal
    total_overdue: Decimal
    
    # Last payment
    last_payment_date: Optional[date]
    last_payment_amount: Optional[Decimal]
    
    # Next payment
    next_payment_due_date: Optional[date]
    next_payment_amount: Optional[Decimal]
    
    # Count
    total_payments: int
    completed_payments: int
    pending_payments: int