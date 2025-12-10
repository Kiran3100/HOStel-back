"""
Fee configuration & breakdown schemas
"""
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.enums import RoomType, FeeType, ChargeType


class ChargesBreakdown(BaseSchema):
    """Breakdown of all components of a fee"""
    base_rent: Decimal
    mess_charges: Decimal
    electricity_charges: Decimal
    water_charges: Decimal
    other_charges: Decimal = Field(Decimal("0.00"))

    total_monthly: Decimal
    total_first_month: Decimal
    security_deposit: Decimal


class FeeConfiguration(BaseSchema):
    """Configuration for calculating total fees for a given booking/student"""
    hostel_id: UUID
    room_type: RoomType
    fee_type: FeeType

    # Components
    base_amount: Decimal
    security_deposit: Decimal
    includes_mess: bool
    mess_charges_monthly: Decimal

    electricity_charges: ChargeType
    electricity_fixed_amount: Optional[Decimal]
    water_charges: ChargeType
    water_fixed_amount: Optional[Decimal]

    # Derived breakdown
    breakdown: ChargesBreakdown