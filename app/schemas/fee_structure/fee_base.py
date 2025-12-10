"""
Base fee structure schemas
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseUpdateSchema
from app.schemas.common.enums import RoomType, FeeType, ChargeType


class FeeStructureBase(BaseSchema):
    """Base fee structure per hostel & room type"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    room_type: RoomType = Field(..., description="Room type to which this fee applies")
    fee_type: FeeType = Field(..., description="Billing frequency")

    amount: Decimal = Field(..., ge=0, description="Base rent amount per period")
    security_deposit: Decimal = Field(Decimal("0.00"), ge=0)

    includes_mess: bool = Field(False, description="Whether mess is included")
    mess_charges_monthly: Decimal = Field(Decimal("0.00"), ge=0)

    # Utility charges
    electricity_charges: ChargeType = Field(
        ChargeType.INCLUDED, description="How electricity is billed"
    )
    electricity_fixed_amount: Optional[Decimal] = Field(None, ge=0)

    water_charges: ChargeType = Field(
        ChargeType.INCLUDED, description="How water is billed"
    )
    water_fixed_amount: Optional[Decimal] = Field(None, ge=0)

    effective_from: date = Field(..., description="Fee effective start date")
    effective_to: Optional[date] = Field(None, description="End date (if any)")

    is_active: bool = Field(True)


class FeeStructureCreate(FeeStructureBase, BaseCreateSchema):
    """Create fee structure entry"""
    pass


class FeeStructureUpdate(BaseUpdateSchema):
    """Update fee structure"""
    amount: Optional[Decimal] = Field(None, ge=0)
    security_deposit: Optional[Decimal] = Field(None, ge=0)
    includes_mess: Optional[bool] = None
    mess_charges_monthly: Optional[Decimal] = Field(None, ge=0)
    electricity_charges: Optional[ChargeType] = None
    electricity_fixed_amount: Optional[Decimal] = Field(None, ge=0)
    water_charges: Optional[ChargeType] = None
    water_fixed_amount: Optional[Decimal] = Field(None, ge=0)
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    is_active: Optional[bool] = None