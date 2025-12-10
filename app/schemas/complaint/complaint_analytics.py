"""
Complaint analytics schemas
"""
from datetime import date
from decimal import Decimal
from typing import Dict, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema


class ComplaintAnalytics(BaseSchema):
    """Comprehensive complaint analytics"""
    hostel_id: Optional[UUID] = None
    period_start: date
    period_end: date
    
    # Summary
    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    closed_complaints: int
    
    # Resolution metrics
    resolution_metrics: "ResolutionMetrics"
    
    # Category analysis
    category_analysis: "CategoryAnalysis"
    
    # Priority distribution
    priority_distribution: Dict[str, int]
    
    # Trend
    complaint_trend: List["ComplaintTrendPoint"]
    
    # SLA performance
    sla_compliance_rate: Decimal
    sla_breached_count: int
    
    # Staff performance
    top_resolvers: List["StaffPerformance"]


class ResolutionMetrics(BaseSchema):
    """Resolution performance metrics"""
    total_resolved: int
    
    # Time metrics
    average_resolution_time_hours: Decimal
    median_resolution_time_hours: Decimal
    fastest_resolution_hours: Decimal
    slowest_resolution_hours: Decimal
    
    # Resolution rate
    resolution_rate: Decimal = Field(..., description="% of complaints resolved")
    same_day_resolution_rate: Decimal
    
    # Escalation
    escalation_rate: Decimal = Field(..., description="% of complaints escalated")
    
    # Reopened
    reopen_rate: Decimal = Field(..., description="% of resolved complaints reopened")


class CategoryAnalysis(BaseSchema):
    """Analysis by complaint category"""
    categories: List["CategoryMetrics"]
    
    most_common_category: str
    most_problematic_category: str = Field(..., description="Category with longest resolution time")


class CategoryMetrics(BaseSchema):
    """Metrics for single category"""
    category: str
    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    
    average_resolution_time_hours: Decimal
    resolution_rate: Decimal
    
    percentage_of_total: Decimal


class ComplaintTrendPoint(BaseSchema):
    """Complaint trend data point"""
    period: str = Field(..., description="Date, week, or month")
    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    
    # By priority
    urgent_count: int
    high_count: int
    medium_count: int
    low_count: int


class StaffPerformance(BaseSchema):
    """Staff complaint resolution performance"""
    staff_id: UUID
    staff_name: str
    staff_role: str
    
    complaints_assigned: int
    complaints_resolved: int
    
    average_resolution_time_hours: Decimal
    resolution_rate: Decimal
    
    average_rating: Optional[Decimal] = None


class ComplaintHeatmap(BaseSchema):
    """Complaint heatmap by time/location"""
    hostel_id: UUID
    
    # By hour of day
    complaints_by_hour: Dict[int, int] = Field(..., description="Hour (0-23) -> count")
    
    # By day of week
    complaints_by_day: Dict[str, int] = Field(..., description="Day -> count")
    
    # By room/floor
    complaints_by_room: List["RoomComplaintCount"]
    complaints_by_floor: Dict[int, int]


class RoomComplaintCount(BaseSchema):
    """Complaint count by room"""
    room_id: UUID
    room_number: str
    complaint_count: int
    
    most_common_category: str