"""
Maintenance analytics schemas
"""
from datetime import date
from decimal import Decimal
from typing import Dict, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class MaintenanceAnalytics(BaseSchema):
    """Comprehensive maintenance analytics"""
    hostel_id: Optional[UUID] = None
    period: DateRangeFilter
    generated_at: datetime
    
    # Summary
    total_requests: int
    completed_requests: int
    pending_requests: int
    
    # Cost
    total_cost: Decimal
    average_cost: Decimal
    
    # Performance
    average_completion_time_hours: Decimal
    completion_rate: Decimal
    
    # Category breakdown
    requests_by_category: Dict[str, int]
    cost_by_category: Dict[str, Decimal]
    
    # Trends
    request_trend: List["TrendPoint"]
    cost_trend: List["CostTrendPoint"]


class TrendPoint(BaseSchema):
    """Trend data point"""
    period: str
    request_count: int
    completed_count: int


class CostTrendPoint(BaseSchema):
    """Cost trend point"""
    period: str
    total_cost: Decimal
    request_count: int
    average_cost: Decimal


class CategoryBreakdown(BaseSchema):
    """Breakdown by category"""
    category: str
    total_requests: int
    completed_requests: int
    total_cost: Decimal
    average_cost: Decimal
    average_completion_time_hours: Decimal


class VendorPerformance(BaseSchema):
    """Vendor performance metrics"""
    vendor_name: str
    
    total_jobs: int
    completed_jobs: int
    on_time_completion_rate: Decimal
    
    average_cost: Decimal
    cost_competitiveness: str  # low/medium/high
    
    quality_rating: Optional[Decimal]
    
    total_spent: Decimal