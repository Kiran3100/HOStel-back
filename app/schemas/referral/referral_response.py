"""
Referral record response schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import ReferralStatus, RewardStatus


class ReferralResponse(BaseResponseSchema):
    """Referral record response"""
    program_id: UUID
    program_name: str

    referrer_id: UUID
    referrer_name: str

    referee_email: Optional[str]
    referee_phone: Optional[str]
    referee_user_id: Optional[UUID]

    referral_code: str
    status: ReferralStatus

    booking_id: Optional[UUID]
    completed_at: Optional[datetime]

    referrer_reward_amount: Optional[Decimal]
    referee_reward_amount: Optional[Decimal]
    currency: str

    referrer_reward_status: RewardStatus
    referee_reward_status: RewardStatus


class ReferralStats(BaseSchema):
    """Referral statistics for a user"""
    user_id: UUID

    total_referrals: int
    successful_referrals: int
    pending_referrals: int

    total_earned: Decimal
    total_paid_out: Decimal
    total_pending_rewards: Decimal