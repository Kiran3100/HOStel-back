"""
Subscription billing schemas
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class BillingCycleInfo(BaseSchema):
    """Info about current billing cycle for subscription"""
    subscription_id: UUID
    hostel_id: UUID
    plan_name: str

    cycle_start: date
    cycle_end: date
    billing_cycle: str  # monthly/yearly

    amount: Decimal
    currency: str

    next_billing_date: date
    auto_renew: bool


class GenerateInvoiceRequest(BaseCreateSchema):
    """Generate invoice for subscription cycle"""
    subscription_id: UUID
    billing_date: date

    # Overridable
    amount_override: Optional[Decimal] = None


class InvoiceInfo(BaseSchema):
    """Generated invoice info"""
    invoice_id: UUID
    subscription_id: UUID
    hostel_id: UUID

    invoice_number: str
    invoice_date: date
    due_date: date

    amount: Decimal
    currency: str

    status: str  # draft, issued, paid, overdue, cancelled
    invoice_url: Optional[str]