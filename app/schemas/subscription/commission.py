"""
Booking commission tracking schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema


class CommissionConfig(BaseSchema):
    """Global/platform commission configuration"""
    default_commission_percentage: Decimal = Field(
        Decimal("5.00"), ge=0, le=100, description="Default commission%"
    )
    min_commission_percentage: Decimal = Field(Decimal("0.00"), ge=0, le=100)
    max_commission_percentage: Decimal = Field(Decimal("30.00"), ge=0, le=100)

    # Per-plan overrides
    commission_by_plan: dict[str, Decimal] = Field(
        default_factory=dict,
        description="plan_type (Standard/Premium) -> commission %",
    )


class BookingCommissionResponse(BaseResponseSchema):
    """Commission record for a booking"""
    booking_id: UUID
    hostel_id: UUID
    subscription_id: UUID

    booking_amount: Decimal
    commission_percentage: Decimal
    commission_amount: Decimal
    currency: str

    status: str  # pending, calculated, paid, waived
    due_date: Optional[date]
    paid_date: Optional[date]
    payment_reference: Optional[str]


class CommissionSummary(BaseSchema):
    """Commission summary for platform/hostel"""
    scope_type: str = Field(..., pattern="^(platform|hostel)$")
    hostel_id: Optional[UUID] = None

    period_start: date
    period_end: date

    total_commission_due: Decimal
    total_commission_paid: Decimal
    total_bookings_count: int
    bookings_with_commission_count: int