# --- File: app/schemas/payment/payment_base.py ---
"""
Payment base schemas with comprehensive validation.

This module defines the core payment schemas including creation,
updates, and base validation logic for the payment lifecycle.
"""

from __future__ import annotations

from datetime import date as Date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.schemas.common.base import BaseCreateSchema, BaseSchema, BaseUpdateSchema
from app.schemas.common.enums import PaymentMethod, PaymentStatus, PaymentType

__all__ = [
    "PaymentBase",
    "PaymentCreate",
    "PaymentUpdate",
]


class PaymentBase(BaseSchema):
    """
    Base payment schema with common fields and validation.
    
    Contains all core payment information including payer details,
    payment type, amount, method, and period information.
    """

    payer_id: UUID = Field(
        ...,
        description="Unique identifier of the user making the payment",
    )
    hostel_id: UUID = Field(
        ...,
        description="Unique identifier of the hostel receiving payment",
    )
    student_id: Optional[UUID] = Field(
        None,
        description="Student profile ID (for recurring fee payments)",
    )
    booking_id: Optional[UUID] = Field(
        None,
        description="Booking ID (for booking-related payments)",
    )

    # Payment Details
    payment_type: PaymentType = Field(
        ...,
        description="Type of payment (rent, deposit, mess, etc.)",
    )
    amount: Decimal = Field(
        ...,
        ge=0,
        description="Payment amount (up to 10 digits with 2 decimal places)",
    )
    currency: str = Field(
        "INR",
        min_length=3,
        max_length=3,
        description="Currency code (ISO 4217)",
    )

    # Payment Period (for recurring fees)
    payment_period_start: Optional[Date] = Field(
        None,
        description="Start Date of the period this payment covers",
    )
    payment_period_end: Optional[Date] = Field(
        None,
        description="End Date of the period this payment covers",
    )

    # Payment Method Details
    payment_method: PaymentMethod = Field(
        ...,
        description="Method of payment (cash, UPI, card, etc.)",
    )
    payment_gateway: Optional[str] = Field(
        None,
        max_length=50,
        description="Payment gateway used (razorpay, stripe, paytm)",
    )

    # Due Date
    due_date: Optional[Date] = Field(
        None,
        description="Payment due Date (for scheduled payments)",
    )

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Validate payment amount is positive and reasonable."""
        if v <= 0:
            raise ValueError("Payment amount must be greater than zero")
        
        # Sanity check: Maximum payment amount
        max_amount = Decimal("1000000.00")  # 10 lakhs
        if v > max_amount:
            raise ValueError(
                f"Payment amount (₹{v}) exceeds maximum allowed (₹{max_amount})"
            )
        
        # Ensure exactly 2 decimal places
        if v.as_tuple().exponent < -2:
            raise ValueError("Payment amount can have at most 2 decimal places")
        
        return v.quantize(Decimal("0.01"))

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        """Validate and normalize currency code."""
        v = v.upper().strip()
        
        # Validate ISO 4217 format (3 uppercase letters)
        if not v.isalpha() or len(v) != 3:
            raise ValueError("Currency must be a valid 3-letter ISO code")
        
        # Currently only support INR
        supported_currencies = ["INR"]
        if v not in supported_currencies:
            raise ValueError(
                f"Currency {v} not supported. Supported: {', '.join(supported_currencies)}"
            )
        
        return v

    @model_validator(mode="after")
    def validate_payment_period(self) -> "PaymentBase":
        """Validate payment period dates if provided."""
        if self.payment_period_start and self.payment_period_end:
            if self.payment_period_end < self.payment_period_start:
                raise ValueError(
                    f"Payment period end ({self.payment_period_end}) must be "
                    f"after or equal to start ({self.payment_period_start})"
                )
            
            # Check period is not too long (max 1 year for single payment)
            days_diff = (self.payment_period_end - self.payment_period_start).days
            if days_diff > 365:
                raise ValueError(
                    f"Payment period cannot exceed 365 days (got {days_diff} days)"
                )
        
        return self

    @model_validator(mode="after")
    def validate_entity_references(self) -> "PaymentBase":
        """Validate entity references are consistent."""
        # At least one of student_id or booking_id should be present for most payment types
        if self.payment_type not in [PaymentType.OTHER]:
            if not self.student_id and not self.booking_id:
                # Warning: Payment should be linked to a student or booking
                # In production, you might want to log this
                pass
        
        return self

    @field_validator("payment_gateway")
    @classmethod
    def validate_payment_gateway(cls, v: Optional[str]) -> Optional[str]:
        """Validate payment gateway if provided."""
        if v is not None:
            v = v.lower().strip()
            
            supported_gateways = ["razorpay", "stripe", "paytm", "phonepe", "googlepay"]
            if v not in supported_gateways:
                raise ValueError(
                    f"Payment gateway '{v}' not supported. "
                    f"Supported: {', '.join(supported_gateways)}"
                )
        
        return v

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[Date]) -> Optional[Date]:
        """Validate due Date is reasonable."""
        if v is not None:
            # Warn if due Date is too far in the past
            days_ago = (Date.today() - v).days
            if days_ago > 365:
                # Log warning - might be data migration
                pass
            
            # Warn if due Date is too far in the future
            days_ahead = (v - Date.today()).days
            if days_ahead > 365:
                # Log warning
                pass
        
        return v

    @property
    def is_overdue(self) -> bool:
        """Check if payment is overdue."""
        if self.due_date is None:
            return False
        return Date.today() > self.due_date

    @property
    def days_overdue(self) -> int:
        """Calculate days overdue (0 if not overdue)."""
        if not self.is_overdue:
            return 0
        return (Date.today() - self.due_date).days  # type: ignore


class PaymentCreate(PaymentBase, BaseCreateSchema):
    """
    Schema for creating a new payment.
    
    Includes all base fields plus creation-specific fields like
    transaction ID and collection details.
    """

    # Additional Creation Fields
    transaction_id: Optional[str] = Field(
        None,
        max_length=100,
        description="External transaction ID from payment gateway or bank",
    )
    collected_by: Optional[UUID] = Field(
        None,
        description="Staff member who collected the payment (for offline payments)",
    )

    # Additional Notes
    notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Additional notes about the payment",
    )

    @field_validator("transaction_id")
    @classmethod
    def validate_transaction_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean transaction ID."""
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
            
            # Ensure it doesn't exceed max length
            if len(v) > 100:
                raise ValueError("Transaction ID cannot exceed 100 characters")
        
        return v

    @model_validator(mode="after")
    def validate_offline_payment(self) -> "PaymentCreate":
        """Validate offline payment requires collection details."""
        offline_methods = [
            PaymentMethod.CASH,
            PaymentMethod.CHEQUE,
            PaymentMethod.BANK_TRANSFER,
        ]
        
        if self.payment_method in offline_methods:
            if not self.collected_by:
                raise ValueError(
                    f"collected_by is required for {self.payment_method.value} payments"
                )
        
        return self

    @field_validator("notes")
    @classmethod
    def clean_notes(cls, v: Optional[str]) -> Optional[str]:
        """Clean notes field."""
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
        return v


class PaymentUpdate(BaseUpdateSchema):
    """
    Schema for updating an existing payment.
    
    All fields are optional, allowing partial updates.
    Primarily used for status updates and adding receipt information.
    """

    payment_status: Optional[PaymentStatus] = Field(
        None,
        description="Update payment status",
    )
    transaction_id: Optional[str] = Field(
        None,
        max_length=100,
        description="Update transaction ID",
    )
    
    # Status Timestamps
    paid_at: Optional[datetime] = Field(
        None,
        description="Timestamp when payment was completed",
    )
    failed_at: Optional[datetime] = Field(
        None,
        description="Timestamp when payment failed",
    )
    failure_reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Reason for payment failure",
    )

    # Receipt Information
    receipt_number: Optional[str] = Field(
        None,
        max_length=50,
        description="Receipt number",
    )
    receipt_url: Optional[str] = Field(
        None,
        description="URL to download receipt",
    )

    # Additional Notes
    notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Update notes",
    )

    @field_validator("failure_reason")
    @classmethod
    def validate_failure_reason(cls, v: Optional[str]) -> Optional[str]:
        """Validate failure reason is meaningful."""
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
            
            if len(v) < 5:
                raise ValueError(
                    "Failure reason must be at least 5 characters if provided"
                )
        
        return v

    @model_validator(mode="after")
    def validate_status_consistency(self) -> "PaymentUpdate":
        """Validate status-related fields are consistent."""
        # If status is COMPLETED, paid_at should be set
        if self.payment_status == PaymentStatus.COMPLETED:
            if not self.paid_at:
                # Set to current time if not provided
                self.paid_at = datetime.utcnow()
        
        # If status is FAILED, failed_at and failure_reason should be set
        if self.payment_status == PaymentStatus.FAILED:
            if not self.failed_at:
                self.failed_at = datetime.utcnow()
            
            if not self.failure_reason:
                raise ValueError(
                    "failure_reason is required when payment_status is FAILED"
                )
        
        return self

    @field_validator("transaction_id", "receipt_number", "notes")
    @classmethod
    def clean_text_fields(cls, v: Optional[str]) -> Optional[str]:
        """Clean text fields."""
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
        return v