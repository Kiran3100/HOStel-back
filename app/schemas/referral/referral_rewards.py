"""
Referral reward tracking schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.common.enums import RewardStatus, PaymentMethod


class RewardConfig(BaseSchema):
    """Global referral reward config (for payouts)"""
    min_payout_amount: Decimal = Field(
        Decimal("100.00"), ge=0, description="Minimum amount before payout"
    )
    payout_methods: List[PaymentMethod] = Field(
        default_factory=lambda: [PaymentMethod.BANK_TRANSFER, PaymentMethod.UPI]
    )


class RewardTracking(BaseSchema):
    """Track rewards for user"""
    user_id: UUID

    total_rewards_earned: Decimal
    total_rewards_paid: Decimal
    pending_rewards: Decimal

    # Breakdown
    rewards_by_program: dict[str, Decimal]


class PayoutRequest(BaseCreateSchema):
    """Request payout of referral rewards"""
    user_id: UUID
    amount: Decimal = Field(..., ge=0)

    payout_method: PaymentMethod
    payout_details: dict = Field(
        ..., description="Method-specific details (UPI ID, bank account, etc.)"
    )


class PayoutRequestResponse(BaseSchema):
    """Payout request status"""
    payout_request_id: UUID
    user_id: UUID
    amount: Decimal
    payout_method: PaymentMethod

    status: RewardStatus
    requested_at: datetime
    processed_at: Optional[datetime]
    failure_reason: Optional[str] = None