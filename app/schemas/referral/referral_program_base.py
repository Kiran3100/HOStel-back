"""
Referral program definition schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema
from app.schemas.common.enums import PaymentType


class ReferralProgramBase(BaseSchema):
    """Base referral program schema"""
    program_name: str = Field(..., min_length=3, max_length=100)
    program_type: str = Field(
        ...,
        pattern="^(student_referral|visitor_referral|affiliate)$",
    )

    reward_type: str = Field(
        ...,
        pattern="^(cash|discount|voucher|free_month)$",
    )
    referrer_reward_amount: Optional[Decimal] = Field(None, ge=0)
    referee_reward_amount: Optional[Decimal] = Field(None, ge=0)
    currency: str = Field("INR", min_length=3, max_length=3)

    min_booking_amount: Optional[Decimal] = Field(None, ge=0)
    min_stay_months: Optional[int] = Field(None, ge=1)

    terms_and_conditions: Optional[str] = Field(None, max_length=5000)

    is_active: bool = Field(True)
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None


class ProgramCreate(ReferralProgramBase, BaseCreateSchema):
    """Create referral program"""
    pass


class ProgramUpdate(BaseUpdateSchema):
    """Update referral program"""
    program_name: Optional[str] = None
    reward_type: Optional[str] = None
    referrer_reward_amount: Optional[Decimal] = Field(None, ge=0)
    referee_reward_amount: Optional[Decimal] = Field(None, ge=0)
    min_booking_amount: Optional[Decimal] = Field(None, ge=0)
    min_stay_months: Optional[int] = Field(None, ge=1)
    terms_and_conditions: Optional[str] = None
    is_active: Optional[bool] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None