"""
Referral tracking schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseResponseSchema, BaseSchema
from app.schemas.common.enums import ReferralStatus, RewardStatus


class ReferralBase(BaseSchema):
    """Base referral record"""
    program_id: UUID
    referrer_id: UUID

    referee_email: Optional[str] = None
    referee_phone: Optional[str] = None
    referee_user_id: Optional[UUID] = None

    referral_code: str = Field(..., max_length=50)
    status: ReferralStatus = Field(ReferralStatus.PENDING)


class ReferralCreate(ReferralBase, BaseCreateSchema):
    """Create referral (generate code or track share)"""
    pass