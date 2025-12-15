# --- File: app/schemas/payment/payment_refund.py ---
"""
Payment refund schemas.

This module defines schemas for refund requests, responses,
status tracking, and approval workflows.
"""

from __future__ import annotations

from datetime import date as Date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import Field, field_validator, model_validator, computed_field

from app.schemas.common.base import BaseCreateSchema, BaseResponseSchema, BaseSchema

__all__ = [
    "RefundRequest",
    "RefundResponse",
    "RefundStatus",
    "RefundApproval",
    "RefundList",
    "RefundListItem",
]


class RefundRequest(BaseCreateSchema):
    """
    Payment refund request schema.
    
    Used to initiate refund of a completed payment.
    """

    payment_id: UUID = Field(
        ...,
        description="Payment ID to refund",
    )
    refund_amount: Decimal = Field(
        ...,
        ge=0,
        description="Amount to refund (must not exceed payment amount)",
    )

    refund_reason: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Detailed reason for refund",
    )

    # Refund Type
    refund_type: str = Field(
        "full",
        pattern=r"^(full|partial)$",
        description="Whether this is a full or partial refund",
    )

    # Refund Method
    refund_method: str = Field(
        "original_source",
        pattern=r"^(original_source|bank_transfer|cash|cheque)$",
        description="How to process the refund",
    )

    # Bank Details (if refund_method is bank_transfer)
    bank_account_number: Optional[str] = Field(
        None,
        max_length=20,
        description="Bank account number for transfer",
    )
    bank_ifsc_code: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{4}0[A-Z0-9]{6}$",
        description="IFSC code for bank transfer",
    )
    account_holder_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Name of account holder",
    )

    # Additional Details
    admin_notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Internal admin notes",
    )

    @field_validator("refund_amount")
    @classmethod
    def validate_refund_amount(cls, v: Decimal) -> Decimal:
        """Validate refund amount is positive."""
        if v <= 0:
            raise ValueError("Refund amount must be greater than zero")
        return v.quantize(Decimal("0.01"))

    @field_validator("refund_reason")
    @classmethod
    def validate_refund_reason(cls, v: str) -> str:
        """Validate refund reason is meaningful."""
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Refund reason must be at least 10 characters")
        return v

    @model_validator(mode="after")
    def validate_bank_details(self) -> "RefundRequest":
        """Validate bank details if refund method is bank transfer."""
        if self.refund_method == "bank_transfer":
            if not all([
                self.bank_account_number,
                self.bank_ifsc_code,
                self.account_holder_name,
            ]):
                raise ValueError(
                    "Bank account details (account_number, IFSC, account_holder_name) "
                    "are required for bank transfer refunds"
                )
        
        return self

    @field_validator("bank_ifsc_code")
    @classmethod
    def validate_ifsc_code(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize IFSC code."""
        if v is not None:
            v = v.upper().strip()
            # IFSC format: 4 letters, 0, then 6 alphanumeric
            if not v or len(v) != 11:
                raise ValueError("IFSC code must be 11 characters")
        return v


class RefundResponse(BaseResponseSchema):
    """
    Refund response after processing refund request.
    
    Contains refund details and processing information.
    """

    refund_id: UUID = Field(
        ...,
        description="Unique refund identifier",
    )
    payment_id: UUID = Field(
        ...,
        description="Original payment ID",
    )
    payment_reference: str = Field(
        ...,
        description="Original payment reference",
    )

    refund_amount: Decimal = Field(
        ...,
        ge=0,
        description="Refund amount",
    )
    refund_status: str = Field(
        ...,
        pattern=r"^(pending|processing|completed|failed)$",
        description="Current refund status",
    )

    # Processing Details
    refund_method: str = Field(
        ...,
        description="Refund method",
    )
    refund_reference: Optional[str] = Field(
        None,
        description="Refund transaction reference number",
    )

    # Timeline
    requested_at: datetime = Field(
        ...,
        description="When refund was requested",
    )
    processed_at: Optional[datetime] = Field(
        None,
        description="When refund processing started",
    )
    completed_at: Optional[datetime] = Field(
        None,
        description="When refund was completed",
    )
    estimated_completion_date: Optional[Date] = Field(
        None,
        description="Estimated completion Date",
    )

    # Destination
    refunded_to: str = Field(
        ...,
        description="Where refund was sent (account details/original source)",
    )

    message: str = Field(
        ...,
        description="User-friendly message about refund status",
    )


class RefundStatus(BaseSchema):
    """
    Refund status tracking schema.
    
    Provides detailed status information about a refund.
    """

    refund_id: UUID = Field(
        ...,
        description="Refund ID",
    )
    payment_reference: str = Field(
        ...,
        description="Original payment reference",
    )

    refund_amount: Decimal = Field(
        ...,
        ge=0,
        description="Refund amount",
    )
    currency: str = Field(
        ...,
        description="Currency code",
    )

    status: str = Field(
        ...,
        pattern=r"^(pending|processing|completed|failed|cancelled)$",
        description="Current refund status",
    )

    # Timeline
    requested_at: datetime = Field(
        ...,
        description="Request timestamp",
    )
    processing_started_at: Optional[datetime] = Field(
        None,
        description="Processing start timestamp",
    )
    completed_at: Optional[datetime] = Field(
        None,
        description="Completion timestamp",
    )

    # Progress Tracking
    days_since_request: int = Field(
        ...,
        ge=0,
        description="Number of days since refund was requested",
    )

    # Failure Details
    failure_reason: Optional[str] = Field(
        None,
        description="Reason for refund failure if applicable",
    )

    # Next Steps
    next_action: Optional[str] = Field(
        None,
        description="Next action required (if any)",
    )
    expected_completion_date: Optional[Date] = Field(
        None,
        description="Expected completion Date",
    )

    @computed_field  # type: ignore[misc]
    @property
    def is_completed(self) -> bool:
        """Check if refund is completed."""
        return self.status == "completed"

    @computed_field  # type: ignore[misc]
    @property
    def is_pending_approval(self) -> bool:
        """Check if refund is pending approval."""
        return self.status == "pending"


class RefundApproval(BaseCreateSchema):
    """
    Refund approval/rejection schema (admin only).
    
    Used by admins to approve or reject refund requests.
    """

    refund_id: UUID = Field(
        ...,
        description="Refund ID to approve/reject",
    )
    approved: bool = Field(
        ...,
        description="Whether to approve (True) or reject (False)",
    )

    # If Approved
    processing_notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Processing notes (visible to staff)",
    )

    # If Rejected
    rejection_reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Reason for rejection (sent to requester)",
    )

    @model_validator(mode="after")
    def validate_approval_fields(self) -> "RefundApproval":
        """Validate approval/rejection fields."""
        if not self.approved and not self.rejection_reason:
            raise ValueError(
                "rejection_reason is required when refund is rejected"
            )
        
        return self

    @field_validator("rejection_reason")
    @classmethod
    def validate_rejection_reason(cls, v: Optional[str]) -> Optional[str]:
        """Validate rejection reason."""
        if v is not None:
            v = v.strip()
            if len(v) < 10:
                raise ValueError(
                    "Rejection reason must be at least 10 characters"
                )
        return v


class RefundListItem(BaseSchema):
    """
    Refund list item for summary views.
    
    Minimal schema for displaying refunds in lists.
    """

    refund_id: UUID = Field(..., description="Refund ID")
    payment_reference: str = Field(..., description="Payment reference")
    student_name: str = Field(..., description="Student/payer name")

    refund_amount: Decimal = Field(
        ...,
        ge=0,
        description="Refund amount",
    )
    status: str = Field(..., description="Refund status")

    requested_at: datetime = Field(..., description="Request timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")

    @computed_field  # type: ignore[misc]
    @property
    def processing_days(self) -> int:
        """Calculate days taken to process."""
        if self.completed_at:
            return (self.completed_at - self.requested_at).days
        return (datetime.utcnow() - self.requested_at).days


class RefundList(BaseSchema):
    """
    List of refunds with summary.
    
    Contains collection of refunds with aggregate information.
    """

    total_refunds: int = Field(
        ...,
        ge=0,
        description="Total number of refunds",
    )
    total_amount_refunded: Decimal = Field(
        ...,
        ge=0,
        description="Total amount refunded",
    )

    refunds: List[RefundListItem] = Field(
        default_factory=list,
        description="List of refund items",
    )

    @computed_field  # type: ignore[misc]
    @property
    def average_refund_amount(self) -> Decimal:
        """Calculate average refund amount."""
        if self.total_refunds == 0:
            return Decimal("0.00")
        return (self.total_amount_refunded / self.total_refunds).quantize(
            Decimal("0.01")
        )