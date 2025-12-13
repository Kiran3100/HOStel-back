# --- File: app/schemas/payment/payment_ledger.py ---
"""
Payment ledger and account statement schemas.

This module defines schemas for financial ledger management including
ledger entries, summaries, statements, and adjustments.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import Field, field_validator, computed_field

from app.schemas.common.base import BaseResponseSchema, BaseSchema

__all__ = [
    "LedgerEntry",
    "LedgerSummary",
    "AccountStatement",
    "TransactionHistory",
    "TransactionItem",
    "BalanceAdjustment",
    "WriteOff",
]


class LedgerEntry(BaseResponseSchema):
    """
    Individual ledger entry.
    
    Represents a single financial transaction in the student's ledger.
    """

    student_id: UUID = Field(
        ...,
        description="Student ID",
    )
    hostel_id: UUID = Field(
        ...,
        description="Hostel ID",
    )

    # Entry Details
    entry_date: date = Field(
        ...,
        description="Date of entry",
    )
    entry_type: str = Field(
        ...,
        pattern=r"^(debit|credit)$",
        description="Entry type (debit increases balance, credit decreases)",
    )

    # Transaction Details
    transaction_type: str = Field(
        ...,
        description="Type of transaction (payment, charge, adjustment, etc.)",
    )
    amount: Decimal = Field(
        ...,
        description="Transaction amount",
    )

    # Running Balance
    balance_before: Decimal = Field(
        ...,
        description="Balance before this entry",
    )
    balance_after: Decimal = Field(
        ...,
        description="Balance after this entry",
    )

    # Reference
    payment_id: Optional[UUID] = Field(
        None,
        description="Associated payment ID",
    )
    payment_reference: Optional[str] = Field(
        None,
        description="Payment reference number",
    )

    # Description
    description: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Entry description",
    )

    # Metadata
    created_by: Optional[UUID] = Field(
        None,
        description="User who created this entry",
    )
    notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Additional notes",
    )

    @computed_field  # type: ignore[misc]
    @property
    def is_debit(self) -> bool:
        """Check if entry is a debit."""
        return self.entry_type == "debit"

    @computed_field  # type: ignore[misc]
    @property
    def is_credit(self) -> bool:
        """Check if entry is a credit."""
        return self.entry_type == "credit"


class LedgerSummary(BaseSchema):
    """
    Ledger summary for a student.
    
    Provides aggregate financial information.
    """

    student_id: UUID = Field(
        ...,
        description="Student ID",
    )
    student_name: str = Field(
        ...,
        description="Student name",
    )
    hostel_id: UUID = Field(
        ...,
        description="Hostel ID",
    )

    # Current Balance
    current_balance: Decimal = Field(
        ...,
        description="Current outstanding balance",
    )

    # Breakdown
    total_charges: Decimal = Field(
        ...,
        ge=0,
        description="Total charges (debits)",
    )
    total_payments: Decimal = Field(
        ...,
        ge=0,
        description="Total payments (credits)",
    )
    total_refunds: Decimal = Field(
        ...,
        ge=0,
        description="Total refunds received",
    )

    # Outstanding
    total_due: Decimal = Field(
        ...,
        ge=0,
        description="Total amount currently due",
    )
    overdue_amount: Decimal = Field(
        ...,
        ge=0,
        description="Amount that is overdue",
    )

    # Last Transaction
    last_transaction_date: Optional[date] = Field(
        None,
        description="Date of last transaction",
    )
    last_payment_date: Optional[date] = Field(
        None,
        description="Date of last payment",
    )

    @computed_field  # type: ignore[misc]
    @property
    def net_amount(self) -> Decimal:
        """Calculate net amount (charges - payments)."""
        return (self.total_charges - self.total_payments).quantize(Decimal("0.01"))

    @computed_field  # type: ignore[misc]
    @property
    def has_overdue_balance(self) -> bool:
        """Check if there's any overdue amount."""
        return self.overdue_amount > Decimal("0")

    @computed_field  # type: ignore[misc]
    @property
    def account_status(self) -> str:
        """
        Determine account status.
        
        Returns: "current", "due", or "overdue"
        """
        if self.overdue_amount > 0:
            return "overdue"
        elif self.total_due > 0:
            return "due"
        else:
            return "current"


class AccountStatement(BaseSchema):
    """
    Account statement for a period.
    
    Detailed statement of all transactions for a student.
    """

    student_id: UUID = Field(
        ...,
        description="Student ID",
    )
    student_name: str = Field(
        ...,
        description="Student name",
    )
    hostel_id: UUID = Field(
        ...,
        description="Hostel ID",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )

    # Statement Period
    statement_period_start: date = Field(
        ...,
        description="Statement period start date",
    )
    statement_period_end: date = Field(
        ...,
        description="Statement period end date",
    )
    generated_at: datetime = Field(
        ...,
        description="When statement was generated",
    )

    # Opening Balance
    opening_balance: Decimal = Field(
        ...,
        description="Balance at start of period",
    )

    # Transactions
    entries: List[LedgerEntry] = Field(
        default_factory=list,
        description="List of ledger entries for the period",
    )

    # Summary
    total_debits: Decimal = Field(
        ...,
        ge=0,
        description="Total debits in period",
    )
    total_credits: Decimal = Field(
        ...,
        ge=0,
        description="Total credits in period",
    )

    # Closing Balance
    closing_balance: Decimal = Field(
        ...,
        description="Balance at end of period",
    )

    # Download Link
    pdf_url: Optional[str] = Field(
        None,
        description="URL to download PDF statement",
    )

    @computed_field  # type: ignore[misc]
    @property
    def net_change(self) -> Decimal:
        """Calculate net change in balance."""
        return (self.closing_balance - self.opening_balance).quantize(Decimal("0.01"))

    @computed_field  # type: ignore[misc]
    @property
    def transaction_count(self) -> int:
        """Get total number of transactions."""
        return len(self.entries)


class TransactionItem(BaseSchema):
    """
    Individual transaction in history.
    
    Simplified transaction for history views.
    """

    transaction_id: UUID = Field(
        ...,
        description="Transaction ID",
    )
    transaction_date: datetime = Field(
        ...,
        description="Transaction timestamp",
    )
    transaction_type: str = Field(
        ...,
        description="Type of transaction",
    )

    amount: Decimal = Field(
        ...,
        description="Transaction amount",
    )
    balance_after: Decimal = Field(
        ...,
        description="Balance after transaction",
    )

    description: str = Field(
        ...,
        description="Transaction description",
    )
    payment_reference: Optional[str] = Field(
        None,
        description="Payment reference if applicable",
    )

    status: str = Field(
        ...,
        description="Transaction status",
    )


class TransactionHistory(BaseSchema):
    """
    Transaction history for a student.
    
    Paginated list of transactions with metadata.
    """

    student_id: UUID = Field(
        ...,
        description="Student ID",
    )

    # Transactions
    transactions: List[TransactionItem] = Field(
        default_factory=list,
        description="List of transactions",
    )

    # Pagination
    total_transactions: int = Field(
        ...,
        ge=0,
        description="Total number of transactions",
    )
    page: int = Field(
        ...,
        ge=1,
        description="Current page number",
    )
    page_size: int = Field(
        ...,
        ge=1,
        description="Items per page",
    )

    @computed_field  # type: ignore[misc]
    @property
    def total_pages(self) -> int:
        """Calculate total pages."""
        if self.page_size == 0:
            return 0
        return (self.total_transactions + self.page_size - 1) // self.page_size


class BalanceAdjustment(BaseSchema):
    """
    Manual balance adjustment (admin only).
    
    Used for corrections, waivers, or special adjustments.
    """

    student_id: UUID = Field(
        ...,
        description="Student ID",
    )
    hostel_id: UUID = Field(
        ...,
        description="Hostel ID",
    )

    # Adjustment Details
    adjustment_type: str = Field(
        ...,
        pattern=r"^(debit|credit)$",
        description="Type of adjustment",
    )
    amount: Decimal = Field(
        ...,
        ge=0,
        description="Adjustment amount",
    )

    # Justification
    reason: str = Field(
        ...,
        min_length=20,
        max_length=500,
        description="Detailed reason for adjustment",
    )

    # Authorization
    adjusted_by: UUID = Field(
        ...,
        description="Admin who made the adjustment",
    )
    adjustment_date: date = Field(
        ...,
        description="Date of adjustment",
    )

    # Documentation
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional notes",
    )

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Validate amount is positive."""
        if v <= 0:
            raise ValueError("Adjustment amount must be greater than zero")
        return v.quantize(Decimal("0.01"))

    @field_validator("reason")
    @classmethod
    def validate_reason(cls, v: str) -> str:
        """Validate reason is detailed."""
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Adjustment reason must be at least 20 characters")
        return v


class WriteOff(BaseSchema):
    """
    Write off outstanding amount.
    
    Used to formally write off uncollectable debts.
    """

    student_id: UUID = Field(
        ...,
        description="Student ID",
    )
    amount: Decimal = Field(
        ...,
        ge=0,
        description="Amount to write off",
    )

    # Justification
    reason: str = Field(
        ...,
        min_length=20,
        max_length=500,
        description="Detailed reason for write-off",
    )

    # Authorization
    approved_by: UUID = Field(
        ...,
        description="Admin who approved write-off",
    )
    approval_date: date = Field(
        ...,
        description="Date of approval",
    )

    # Documentation
    supporting_documents: List[str] = Field(
        default_factory=list,
        description="URLs to supporting documents",
    )

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Validate amount."""
        if v <= 0:
            raise ValueError("Write-off amount must be greater than zero")
        return v.quantize(Decimal("0.01"))

    @field_validator("reason")
    @classmethod
    def validate_reason(cls, v: str) -> str:
        """Validate reason is detailed."""
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Write-off reason must be at least 20 characters")
        return v