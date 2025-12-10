"""
Dashboard-level analytics schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional, Dict

from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class KPIResponse(BaseSchema):
    """Single KPI item for dashboard"""
    name: str = Field(..., description="KPI name, e.g., 'Total Revenue'")
    value: Decimal | int | float = Field(..., description="KPI numeric value")
    unit: Optional[str] = Field(None, description="Unit, e.g., 'INR', '%', 'students'")
    trend_direction: Optional[str] = Field(
        None,
        pattern="^(up|down|stable)$",
        description="Trend indicator vs previous period",
    )
    trend_percentage: Optional[Decimal] = Field(
        None, description="Change vs previous period in %"
    )
    target_value: Optional[Decimal] = Field(None, description="Target/goal value")
    good_when: Optional[str] = Field(
        None,
        description="Interpretation rule, e.g. 'higher_is_better', 'lower_is_better'",
    )


class QuickStats(BaseSchema):
    """Quick statistics for main dashboard cards"""
    total_hostels: int
    active_hostels: int
    total_students: int
    active_students: int
    total_visitors: int

    todays_check_ins: int
    todays_check_outs: int

    open_complaints: int
    pending_maintenance: int

    todays_revenue: Decimal
    monthly_revenue: Decimal
    outstanding_payments: Decimal


class DashboardMetrics(BaseSchema):
    """Aggregated dashboard metrics for a given scope (hostel or platform)"""
    scope_type: str = Field(..., pattern="^(hostel|platform|admin)$")
    scope_id: Optional[UUID] = Field(
        None, description="Hostel ID or admin ID if scope_type is not 'platform'"
    )

    period: DateRangeFilter = Field(..., description="Analysis period")
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # KPIs
    kpis: List[KPIResponse] = Field(default_factory=list)

    # Quick stats
    quick_stats: QuickStats

    # Time series for charts
    revenue_timeseries: List["TimeseriesPoint"] = Field(default_factory=list)
    occupancy_timeseries: List["TimeseriesPoint"] = Field(default_factory=list)
    booking_timeseries: List["TimeseriesPoint"] = Field(default_factory=list)
    complaint_timeseries: List["TimeseriesPoint"] = Field(default_factory=list)


class TimeseriesPoint(BaseSchema):
    """Generic timeseries data point"""
    date: date
    value: Decimal | int | float


class RoleSpecificDashboard(BaseSchema):
    """Dashboard sections per role"""
    role: str = Field(..., pattern="^(super_admin|hostel_admin|supervisor)$")
    cards: Dict[str, QuickStats] = Field(
        default_factory=dict, description="Section name -> QuickStats"
    )
    kpis: Dict[str, List[KPIResponse]] = Field(
        default_factory=dict, description="Section name -> list of KPIs"
    )