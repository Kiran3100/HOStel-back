"""
Subscription upgrade/downgrade schemas
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.common.enums import BillingCycle


class UpgradeRequest(BaseCreateSchema):
    """Request to change subscription plan"""
    hostel_id: UUID
    current_plan_id: UUID
    new_plan_id: UUID
    billing_cycle: BillingCycle = Field(...)

    # Timing
    effective_from: date = Field(..., description="When new plan takes effect")
    prorate: bool = Field(True, description="Prorate charges/refunds")


class UpgradePreview(BaseSchema):
    """Preview cost impact of upgrade/downgrade"""
    current_plan_name: str
    new_plan_name: str

    current_amount: Decimal
    new_amount: Decimal

    # For current period
    prorated_charge: Decimal = Field(..., description="Additional amount to charge")
    prorated_refund: Decimal = Field(..., description="If downgrade, refund amount")

    effective_from: date
    message: str


class DowngradeRequest(UpgradeRequest):
    """Same payload, semantics are downgrade if new plan is smaller"""
    pass