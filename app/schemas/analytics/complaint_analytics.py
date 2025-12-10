"""
High-level complaint analytics schemas (dashboard aggregation)
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Optional

from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class ComplaintKPI(BaseSchema):
    """Complaint key performance indicators"""
    hostel_id: Optional[UUID] = None
    hostel_name: Optional[str] = None

    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    closed_complaints: int

    average_resolution_time_hours: Decimal
    sla_compliance_rate: Decimal
    escalation_rate: Decimal
    reopen_rate: Decimal


class ComplaintTrend(BaseSchema):
    """Trend over time for complaints"""
    period: DateRangeFilter
    points: List["ComplaintTrendPoint"] = Field(default_factory=list)


class ComplaintTrendPoint(BaseSchema):
    """Complaint trend point"""
    date: date
    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    escalated: int
    sla_breached: int


class CategoryBreakdown(BaseSchema):
    """Complaints by category"""
    category: str
    count: int
    percentage_of_total: Decimal
    average_resolution_time_hours: Decimal


class ComplaintDashboard(BaseSchema):
    """Complaint dashboard analytics"""
    hostel_id: Optional[UUID] = None
    hostel_name: Optional[str] = None

    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    kpi: ComplaintKPI
    trend: ComplaintTrend
    by_category: List[CategoryBreakdown] = Field(default_factory=list)
    by_priority: Dict[str, int] = Field(default_factory=dict)