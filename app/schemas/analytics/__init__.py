"""
Analytics schemas package
"""

from app.schemas.analytics.dashboard_analytics import (
    DashboardMetrics,
    KPIResponse,
    QuickStats,
)
from app.schemas.analytics.financial_analytics import (
    FinancialReport,
    RevenueBreakdown,
    ExpenseBreakdown,
    ProfitAndLossReport,
    CashflowSummary,
)
from app.schemas.analytics.occupancy_analytics import (
    OccupancyReport,
    OccupancyKPI,
    OccupancyTrendPoint,
    ForecastData,
)
from app.schemas.analytics.complaint_analytics import (
    ComplaintKPI,
    ComplaintDashboard,
    ComplaintTrend,
)
from app.schemas.analytics.visitor_analytics import (
    VisitorFunnel,
    TrafficSourceAnalytics,
    VisitorBehaviorAnalytics,
)
from app.schemas.analytics.booking_analytics import (
    BookingFunnel,
    BookingKPI,
    BookingTrendPoint,
    CancellationAnalytics,
)
from app.schemas.analytics.supervisor_analytics import (
    SupervisorKPI,
    SupervisorDashboardAnalytics,
    SupervisorComparison,
)
from app.schemas.analytics.platform_analytics import (
    PlatformMetrics,
    GrowthMetrics,
    PlatformUsageAnalytics,
)
from app.schemas.analytics.custom_reports import (
    CustomReportRequest,
    CustomReportDefinition,
    CustomReportResult,
)

__all__ = [
    # Dashboard
    "DashboardMetrics",
    "KPIResponse",
    "QuickStats",
    # Financial
    "FinancialReport",
    "RevenueBreakdown",
    "ExpenseBreakdown",
    "ProfitAndLossReport",
    "CashflowSummary",
    # Occupancy
    "OccupancyReport",
    "OccupancyKPI",
    "OccupancyTrendPoint",
    "ForecastData",
    # Complaints
    "ComplaintKPI",
    "ComplaintDashboard",
    "ComplaintTrend",
    # Visitor
    "VisitorFunnel",
    "TrafficSourceAnalytics",
    "VisitorBehaviorAnalytics",
    # Booking
    "BookingFunnel",
    "BookingKPI",
    "BookingTrendPoint",
    "CancellationAnalytics",
    # Supervisor
    "SupervisorKPI",
    "SupervisorDashboardAnalytics",
    "SupervisorComparison",
    # Platform
    "PlatformMetrics",
    "GrowthMetrics",
    "PlatformUsageAnalytics",
    # Custom reports
    "CustomReportRequest",
    "CustomReportDefinition",
    "CustomReportResult",
]