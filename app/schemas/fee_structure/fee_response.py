"""
Fee structure response schemas
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import RoomType, FeeType, ChargeType


class FeeStructureResponse(BaseResponseSchema):
    """Fee structure response"""
    hostel_id: UUID
    hostel_name: str

    room_type: RoomType
    fee_type: FeeType

    amount: Decimal
    security_deposit: Decimal

    includes_mess: bool
    mess_charges_monthly: Decimal

    electricity_charges: ChargeType
    electricity_fixed_amount: Optional[Decimal]

    water_charges: ChargeType
    water_fixed_amount: Optional[Decimal]

    effective_from: date
    effective_to: Optional[date]
    is_active: bool


class FeeDetail(BaseSchema):
    """Full fee detail for a room type (assembled for UI)"""
    room_type: RoomType
    fee_type: FeeType
    amount: Decimal
    security_deposit: Decimal
    includes_mess: bool
    mess_charges_monthly: Decimal
    total_first_month_payable: Decimal
    total_recurring_monthly: Decimal


class FeeStructureList(BaseSchema):
    """List of fee structures for a hostel"""
    hostel_id: UUID
    hostel_name: str
    items: List[FeeStructureResponse] = Field(default_factory=list)