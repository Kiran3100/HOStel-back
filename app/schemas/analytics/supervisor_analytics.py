"""
Supervisor analytics schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class SupervisorKPI(BaseSchema):
    """Supervisor KPI metrics (aggregated)"""
    supervisor_id: UUID
    supervisor_name: str
    hostel_id: UUID
    hostel_name: str

    period: DateRangeFilter

    # Workload
    complaints_assigned: int
    complaints_resolved: int
    maintenance_requests_created: int
    maintenance_requests_completed: int
    attendance_records_marked: int

    # Performance
    avg_complaint_resolution_time_hours: Decimal
    avg_maintenance_completion_time_hours: Decimal
    complaint_sla_compliance_rate: Decimal
    maintenance_sla_compliance_rate: Decimal

    student_feedback_score: Optional[Decimal] = Field(
        None, description="Average rating from student feedback"
    )

    overall_performance_score: Decimal = Field(
        ..., ge=0, le=100, description="Composite performance score"
    )


class SupervisorTrendPoint(BaseSchema):
    """Trend point for supervisor performance"""
    period_label: str
    complaints_resolved: int
    maintenance_completed: int
    performance_score: Decimal


class SupervisorDashboardAnalytics(BaseSchema):
    """Supervisor dashboard analytics"""
    supervisor_id: UUID
    supervisor_name: str
    hostel_id: UUID
    hostel_name: str

    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    kpi: SupervisorKPI
    trend: List[SupervisorTrendPoint] = Field(default_factory=list)

    # Breakdown
    complaints_by_category: Dict[str, int] = Field(default_factory=dict)
    maintenance_by_category: Dict[str, int] = Field(default_factory=dict)


class SupervisorComparison(BaseSchema):
    """Compare supervisors within hostel or platform"""
    scope_type: str = Field(..., pattern="^(hostel|platform)$")
    hostel_id: Optional[UUID] = None

    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    supervisors: List[SupervisorKPI] = Field(default_factory=list)

    # Rankings
    ranked_by_performance: List[UUID] = Field(default_factory=list)
    ranked_by_resolution_speed: List[UUID] = Field(default_factory=list)
    ranked_by_feedback_score: List[UUID] = Field(default_factory=list)