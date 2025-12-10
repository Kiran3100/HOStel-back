"""
Payment refund schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class RefundRequest(BaseCreateSchema):
    """Request payment refund"""
    payment_id: UUID = Field(..., description="Payment ID to refund")
    refund_amount: Decimal = Field(..., ge=0, description="Amount to refund")
    
    refund_reason: str = Field(..., min_length=10, max_length=500, description="Reason for refund")
    
    # Refund type
    refund_type: str = Field(
        "full",
        pattern="^(full|partial)$",
        description="Full or partial refund"
    )
    
    # Processing
    refund_method: str = Field(
        "original_source",
        pattern="^(original_source|bank_transfer|cash|cheque)$",
        description="How to refund"
    )
    
    # Bank details (if bank_transfer)
    bank_account_number: Optional[str] = Field(None, description="Bank account number")
    bank_ifsc_code: Optional[str] = Field(None, description="IFSC code")
    account_holder_name: Optional[str] = Field(None, description="Account holder name")
    
    # Additional details
    admin_notes: Optional[str] = Field(None, max_length=500)


class RefundResponse(BaseResponseSchema):
    """Refund response"""
    refund_id: UUID
    payment_id: UUID
    payment_reference: str
    
    refund_amount: Decimal
    refund_status: str = Field(..., pattern="^(pending|processing|completed|failed)$")
    
    # Processing details
    refund_method: str
    refund_reference: Optional[str] = Field(None, description="Refund transaction reference")
    
    # Timeline
    requested_at: datetime
    processed_at: Optional[datetime]
    completed_at: Optional[datetime]
    estimated_completion_date: Optional[date]
    
    # Refund to
    refunded_to: str = Field(..., description="Destination of refund")
    
    message: str


class RefundStatus(BaseSchema):
    """Refund status tracking"""
    refund_id: UUID
    payment_reference: str
    
    refund_amount: Decimal
    currency: str
    
    status: str = Field(..., pattern="^(pending|processing|completed|failed|cancelled)$")
    
    # Timeline
    requested_at: datetime
    processing_started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    # Days elapsed
    days_since_request: int
    
    # Failure details
    failure_reason: Optional[str] = None
    
    # Next steps
    next_action: Optional[str] = None
    expected_completion_date: Optional[date] = None


class RefundApproval(BaseCreateSchema):
    """Approve refund request (admin)"""
    refund_id: UUID
    approved: bool
    
    # If approved
    processing_notes: Optional[str] = None
    
    # If rejected
    rejection_reason: Optional[str] = None


class RefundList(BaseSchema):
    """List of refunds"""
    total_refunds: int
    total_amount_refunded: Decimal
    
    refunds: List["RefundListItem"]


class RefundListItem(BaseSchema):
    """Refund list item"""
    refund_id: UUID
    payment_reference: str
    student_name: str
    
    refund_amount: Decimal
    status: str
    
    requested_at: datetime
    completed_at: Optional[datetime]