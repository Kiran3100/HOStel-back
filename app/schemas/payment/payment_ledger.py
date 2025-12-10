"""
Payment ledger and account statement schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseResponseSchema


class LedgerEntry(BaseResponseSchema):
    """Individual ledger entry"""
    student_id: UUID
    hostel_id: UUID
    
    entry_date: date
    entry_type: str = Field(..., pattern="^(debit|credit)$")
    
    # Transaction details
    transaction_type: str = Field(..., description="Type of transaction")
    amount: Decimal
    
    # Running balance
    balance_before: Decimal
    balance_after: Decimal
    
    # Reference
    payment_id: Optional[UUID] = None
    payment_reference: Optional[str] = None
    
    description: str
    
    # Metadata
    created_by: Optional[UUID] = None
    notes: Optional[str] = None


class LedgerSummary(BaseSchema):
    """Ledger summary for student"""
    student_id: UUID
    student_name: str
    hostel_id: UUID
    
    # Current balance
    current_balance: Decimal
    
    # Breakdown
    total_charges: Decimal
    total_payments: Decimal
    total_refunds: Decimal
    
    # Outstanding
    total_due: Decimal
    overdue_amount: Decimal
    
    # Last transaction
    last_transaction_date: Optional[date]
    last_payment_date: Optional[date]


class AccountStatement(BaseSchema):
    """Account statement for period"""
    student_id: UUID
    student_name: str
    hostel_id: UUID
    hostel_name: str
    
    statement_period_start: date
    statement_period_end: date
    generated_at: datetime
    
    # Opening balance
    opening_balance: Decimal
    
    # Transactions
    entries: List[LedgerEntry]
    
    # Summary
    total_debits: Decimal
    total_credits: Decimal
    
    # Closing balance
    closing_balance: Decimal
    
    # Download link
    pdf_url: Optional[str] = None


class TransactionHistory(BaseSchema):
    """Transaction history"""
    student_id: UUID
    
    transactions: List["TransactionItem"]
    
    # Pagination
    total_transactions: int
    page: int
    page_size: int


class TransactionItem(BaseSchema):
    """Individual transaction in history"""
    transaction_id: UUID
    transaction_date: datetime
    transaction_type: str
    
    amount: Decimal
    balance_after: Decimal
    
    description: str
    payment_reference: Optional[str]
    
    status: str


class BalanceAdjustment(BaseSchema):
    """Manual balance adjustment (admin only)"""
    student_id: UUID
    hostel_id: UUID
    
    adjustment_type: str = Field(..., pattern="^(debit|credit)$")
    amount: Decimal = Field(..., ge=0)
    
    reason: str = Field(..., min_length=20, max_length=500)
    
    adjusted_by: UUID
    adjustment_date: date
    
    notes: Optional[str] = None


class WriteOff(BaseSchema):
    """Write off outstanding amount"""
    student_id: UUID
    amount: Decimal = Field(..., ge=0)
    
    reason: str = Field(..., min_length=20, max_length=500)
    
    approved_by: UUID
    approval_date: date
    
    # Documentation
    supporting_documents: List[str] = Field(default_factory=list)