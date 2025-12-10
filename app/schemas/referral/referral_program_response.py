"""
Referral program response schemas
"""
from datetime import date
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema


class ProgramResponse(BaseResponseSchema):
    """Referral program response"""
    program_name: str
    program_type: str
    reward_type: str
    referrer_reward_amount: Optional[Decimal]
    referee_reward_amount: Optional[Decimal]
    currency: str

    min_booking_amount: Optional[Decimal]
    min_stay_months: Optional[int]

    is_active: bool
    valid_from: Optional[date]
    valid_to: Optional[date]

    terms_and_conditions: Optional[str]


class ProgramList(BaseSchema):
    """List of active programs"""
    programs: List[ProgramResponse]