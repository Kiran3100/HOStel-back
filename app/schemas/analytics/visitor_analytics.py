"""
Visitor & funnel analytics schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.enums import SearchSource
from app.schemas.common.filters import DateRangeFilter


class VisitorFunnel(BaseSchema):
    """Visitor funnel from views → registration → booking"""
    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Counts
    total_visits: int
    unique_visitors: int
    registrations: int
    bookings: int

    # Conversion rates
    visit_to_registration_rate: Decimal
    registration_to_booking_rate: Decimal
    visit_to_booking_rate: Decimal

    # Drop-off points
    dropped_after_search: int
    dropped_after_hostel_view: int
    dropped_after_booking_start: int


class TrafficSourceAnalytics(BaseSchema):
    """Traffic sources for visitor acquisition"""
    period: DateRangeFilter
    total_visits: int

    visits_by_source: Dict[SearchSource, int] = Field(default_factory=dict)
    registrations_by_source: Dict[SearchSource, int] = Field(default_factory=dict)
    bookings_by_source: Dict[SearchSource, int] = Field(default_factory=dict)

    # Conversion by source
    visit_to_booking_rate_by_source: Dict[SearchSource, Decimal] = Field(
        default_factory=dict
    )


class VisitorBehaviorAnalytics(BaseSchema):
    """Behavior analytics for visitors"""
    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Search behavior
    average_searches_per_session: Decimal
    average_filters_used: Decimal
    most_searched_cities: List[str] = Field(default_factory=list)
    most_filtered_amenities: List[str] = Field(default_factory=list)

    # Engagement
    average_hostels_viewed_per_session: Decimal
    average_time_on_hostel_page_seconds: Decimal
    comparison_tool_usage_rate: Decimal

    # Exit pages
    common_exit_reasons: List[str] = Field(default_factory=list)