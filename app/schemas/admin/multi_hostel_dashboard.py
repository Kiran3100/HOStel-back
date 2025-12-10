"""
Multi-hostel dashboard schemas
"""
from datetime import date
from decimal import Decimal
from typing import List, Dict
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema


class MultiHostelDashboard(BaseSchema):
    """Unified dashboard for multi-hostel admin"""
    admin_id: UUID
    admin_name: str
    total_hostels_managed: int
    
    # Aggregated statistics
    aggregated_stats: "AggregatedStats"
    
    # Individual hostel quick stats
    hostel_stats: List["HostelQuickStats"]
    
    # Cross-hostel comparisons
    comparisons: "CrossHostelComparison"
    
    # Consolidated notifications
    total_notifications: int
    notifications_by_hostel: Dict[UUID, int]
    
    # Consolidated pending tasks
    total_pending_tasks: int
    tasks_by_hostel: Dict[UUID, "HostelTaskSummary"]


class AggregatedStats(BaseSchema):
    """Aggregated statistics across all hostels"""
    # Occupancy
    total_beds: int
    total_occupied: int
    total_available: int
    average_occupancy_percentage: Decimal
    
    # Students
    total_students: int
    active_students: int
    
    # Revenue
    total_revenue_this_month: Decimal
    total_outstanding: Decimal
    total_overdue: Decimal
    
    # Bookings
    total_pending_bookings: int
    total_confirmed_bookings: int
    booking_conversion_rate: Decimal
    
    # Complaints
    total_open_complaints: int
    total_resolved_this_month: int
    average_resolution_time_hours: Decimal
    
    # Maintenance
    total_pending_maintenance: int
    total_completed_this_month: int
    
    # Performance
    average_rating_across_hostels: Decimal
    total_reviews: int


class HostelQuickStats(BaseSchema):
    """Quick statistics for individual hostel"""
    hostel_id: UUID
    hostel_name: str
    hostel_city: str
    
    # Occupancy
    occupancy_percentage: Decimal
    available_beds: int
    
    # Revenue
    revenue_this_month: Decimal
    outstanding_amount: Decimal
    
    # Alerts
    pending_bookings: int
    open_complaints: int
    pending_maintenance: int
    overdue_payments_count: int
    
    # Status indicators
    status_color: str = Field(
        ...,
        pattern="^(green|yellow|red)$",
        description="Overall health status"
    )
    
    # Last activity
    last_supervisor_activity: Optional[datetime]


class CrossHostelComparison(BaseSchema):
    """Comparison metrics across hostels"""
    # Best performers
    highest_occupancy_hostel: "TopPerformer"
    highest_revenue_hostel: "TopPerformer"
    highest_rated_hostel: "TopPerformer"
    
    # Areas needing attention
    lowest_occupancy_hostel: "BottomPerformer"
    most_complaints_hostel: "BottomPerformer"
    most_overdue_payments_hostel: "BottomPerformer"
    
    # Comparative metrics
    occupancy_comparison: List["HostelMetricComparison"]
    revenue_comparison: List["HostelMetricComparison"]
    complaint_rate_comparison: List["HostelMetricComparison"]


class TopPerformer(BaseSchema):
    """Top performing hostel"""
    hostel_id: UUID
    hostel_name: str
    metric_value: Decimal
    metric_name: str


class BottomPerformer(BaseSchema):
    """Bottom performing hostel (needs attention)"""
    hostel_id: UUID
    hostel_name: str
    metric_value: Decimal
    metric_name: str
    issue_severity: str = Field(..., pattern="^(low|medium|high|critical)$")


class HostelMetricComparison(BaseSchema):
    """Individual hostel metric for comparison"""
    hostel_id: UUID
    hostel_name: str
    metric_value: Decimal
    percentage_of_best: Decimal
    trend: str = Field(..., pattern="^(up|down|stable)$")


class HostelTaskSummary(BaseSchema):
    """Task summary for a hostel"""
    hostel_id: UUID
    urgent_tasks: int
    high_priority_tasks: int
    medium_priority_tasks: int
    low_priority_tasks: int
    total_tasks: int