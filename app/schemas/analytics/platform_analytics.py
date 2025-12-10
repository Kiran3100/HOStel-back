"""
Platform-wide analytics (super admin)
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List

from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class PlatformMetrics(BaseSchema):
    """High-level platform metrics"""
    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Tenants
    total_hostels: int
    active_hostels: int
    hostels_on_trial: int

    # Users
    total_users: int
    total_students: int
    total_supervisors: int
    total_admins: int
    total_visitors: int

    # Load
    avg_daily_active_users: int
    peak_concurrent_sessions: int


class GrowthMetrics(BaseSchema):
    """Growth metrics over time"""
    period: DateRangeFilter

    # Hostels
    new_hostels: int
    churned_hostels: int
    net_hostel_growth: int

    # Revenue
    total_revenue: Decimal
    revenue_growth_rate: Decimal

    # Users
    new_users: int
    user_growth_rate: Decimal

    # Charts
    monthly_revenue: List["MonthlyMetric"] = Field(default_factory=list)
    monthly_new_hostels: List["MonthlyMetric"] = Field(default_factory=list)
    monthly_new_users: List["MonthlyMetric"] = Field(default_factory=list)


class MonthlyMetric(BaseSchema):
    """Monthly metric point"""
    month: str  # YYYY-MM
    value: Decimal | int | float


class PlatformUsageAnalytics(BaseSchema):
    """Platform usage analytics"""
    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Traffic
    total_requests: int
    avg_requests_per_minute: Decimal
    api_error_rate: Decimal

    # By endpoint group
    requests_by_module: Dict[str, int] = Field(
        default_factory=dict, description="module -> request count"
    )

    # Latency
    avg_response_time_ms: Decimal
    p95_response_time_ms: Decimal
    p99_response_time_ms: Decimal

    # Resource usage (if tracked)
    avg_cpu_usage_percent: Optional[Decimal] = None
    avg_memory_usage_percent: Optional[Decimal] = None