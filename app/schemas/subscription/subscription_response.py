"""
Subscription response schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import SubscriptionStatus, BillingCycle, SubscriptionPlan


class SubscriptionResponse(BaseResponseSchema):
    """Hostel subscription response"""
    hostel_id: UUID
    hostel_name: str

    plan_id: UUID
    plan_name: str
    display_name: str
    plan_type: SubscriptionPlan

    subscription_reference: str
    billing_cycle: BillingCycle
    amount: Decimal
    currency: str

    start_date: date
    end_date: date
    auto_renew: bool
    next_billing_date: Optional[date]
    status: SubscriptionStatus

    trial_end_date: Optional[date]
    last_payment_date: Optional[date]
    last_payment_amount: Optional[Decimal]


class BillingHistoryItem(BaseSchema):
    """Single billing event"""
    billing_date: date
    amount: Decimal
    currency: str
    status: str
    payment_reference: Optional[str]
    invoice_url: Optional[str]


class BillingHistory(BaseSchema):
    """Subscription billing history"""
    subscription_id: UUID
    hostel_id: UUID

    items: list[BillingHistoryItem]
    total_billed: Decimal
    total_paid: Decimal
    total_outstanding: Decimal