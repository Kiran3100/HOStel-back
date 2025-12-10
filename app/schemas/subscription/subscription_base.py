"""
Hostel subscription schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema, BaseSchema
from app.schemas.common.enums import SubscriptionStatus, BillingCycle


class SubscriptionBase(BaseSchema):
    """Base subscription for a hostel"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    plan_id: UUID = Field(..., description="Subscription plan ID")

    subscription_reference: str = Field(..., max_length=100)

    billing_cycle: BillingCycle = Field(..., description="Billing cycle (monthly/yearly)")
    amount: Decimal = Field(..., ge=0, description="Amount per billing period")
    currency: str = Field("INR", min_length=3, max_length=3)

    # Period
    start_date: date = Field(..., description="Subscription start date")
    end_date: date = Field(..., description="Subscription end date")

    auto_renew: bool = Field(True)
    next_billing_date: Optional[date] = None

    status: SubscriptionStatus = Field(SubscriptionStatus.ACTIVE)


class SubscriptionCreate(SubscriptionBase, BaseCreateSchema):
    """Create new hostel subscription"""
    trial_end_date: Optional[date] = None


class SubscriptionUpdate(BaseUpdateSchema):
    """Update subscription (e.g. status, next billing)"""
    status: Optional[SubscriptionStatus] = None
    end_date: Optional[date] = None
    auto_renew: Optional[bool] = None
    next_billing_date: Optional[date] = None