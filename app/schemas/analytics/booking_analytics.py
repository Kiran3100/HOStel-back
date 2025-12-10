"""
Booking analytics schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Optional

from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.enums import BookingStatus, BookingSource
from app.schemas.common.filters import DateRangeFilter


class BookingKPI(BaseSchema):
    """Key metrics for bookings"""
    hostel_id: Optional[UUID] = None
    hostel_name: Optional[str] = None

    total_bookings: int
    confirmed_bookings: int
    cancelled_bookings: int
    rejected_bookings: int

    booking_conversion_rate: Decimal
    cancellation_rate: Decimal
    average_lead_time_days: Decimal  # between booking and check-in


class BookingTrendPoint(BaseSchema):
    """Booking trend point"""
    date: date
    total_bookings: int
    confirmed: int
    cancelled: int
    rejected: int
    revenue_for_day: Decimal


class BookingFunnel(BaseSchema):
    """Booking funnel analytics"""
    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Steps in funnel
    hostel_page_views: int
    booking_form_starts: int
    booking_submissions: int
    bookings_confirmed: int

    # Conversion
    view_to_start_rate: Decimal
    start_to_submit_rate: Decimal
    submit_to_confirm_rate: Decimal
    view_to_confirm_rate: Decimal


class CancellationAnalytics(BaseSchema):
    """Analytics around cancellations"""
    period: DateRangeFilter
    total_cancellations: int
    cancellation_rate: Decimal

    cancellations_by_reason: Dict[str, int] = Field(default_factory=dict)
    cancellations_by_status: Dict[BookingStatus, int] = Field(default_factory=dict)

    # Timing
    average_time_before_check_in_cancelled_days: Decimal


class BookingAnalyticsSummary(BaseSchema):
    """Top-level booking analytics"""
    hostel_id: Optional[UUID] = None
    hostel_name: Optional[str] = None

    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    kpi: BookingKPI
    trend: List[BookingTrendPoint] = Field(default_factory=list)

    funnel: BookingFunnel
    cancellations: CancellationAnalytics

    # By source
    bookings_by_source: Dict[BookingSource, int] = Field(default_factory=dict)
    conversion_rate_by_source: Dict[BookingSource, Decimal] = Field(default_factory=dict)