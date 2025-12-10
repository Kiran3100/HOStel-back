"""
Hostel analytics and reporting schemas
"""
from decimal import Decimal
from datetime import date, datetime
from typing import List, Optional, Dict
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class HostelAnalytics(BaseSchema):
    """Comprehensive hostel analytics"""
    hostel_id: UUID
    hostel_name: str
    period_start: date
    period_end: date
    
    occupancy: "OccupancyAnalytics"
    revenue: "RevenueAnalytics"
    bookings: "BookingAnalytics"
    complaints: "ComplaintAnalytics"
    reviews: "ReviewAnalytics"
    generated_at: datetime


class OccupancyAnalytics(BaseSchema):
    """Occupancy analytics"""
    current_occupancy_rate: Decimal = Field(..., description="Current occupancy %")
    average_occupancy_rate: Decimal = Field(..., description="Average for period")
    peak_occupancy_rate: Decimal = Field(..., description="Peak occupancy")
    lowest_occupancy_rate: Decimal = Field(..., description="Lowest occupancy")
    
    total_beds: int
    occupied_beds: int
    available_beds: int
    
    # Trends
    occupancy_trend: List["OccupancyDataPoint"] = Field(default_factory=list)
    
    # Predictions
    predicted_occupancy_next_month: Optional[Decimal] = None


class OccupancyDataPoint(BaseSchema):
    """Occupancy data point for trends"""
    date: date
    occupancy_rate: Decimal
    occupied_beds: int
    total_beds: int


class RevenueAnalytics(BaseSchema):
    """Revenue analytics"""
    total_revenue: Decimal = Field(..., description="Total revenue for period")
    rent_revenue: Decimal
    mess_revenue: Decimal
    other_revenue: Decimal
    
    total_collected: Decimal
    total_pending: Decimal
    total_overdue: Decimal
    
    collection_rate: Decimal = Field(..., description="Payment collection rate %")
    
    # Trends
    revenue_trend: List["RevenueDataPoint"] = Field(default_factory=list)
    
    # Comparison
    revenue_vs_last_period: Decimal = Field(..., description="% change from last period")
    revenue_vs_last_year: Optional[Decimal] = None


class RevenueDataPoint(BaseSchema):
    """Revenue data point"""
    date: date
    revenue: Decimal
    collected: Decimal
    pending: Decimal


class BookingAnalytics(BaseSchema):
    """Booking analytics"""
    total_bookings: int
    approved_bookings: int
    pending_bookings: int
    rejected_bookings: int
    cancelled_bookings: int
    
    conversion_rate: Decimal = Field(..., description="Booking approval rate %")
    cancellation_rate: Decimal = Field(..., description="Cancellation rate %")
    
    # Sources
    booking_sources: Dict[str, int] = Field(default_factory=dict)
    
    # Trends
    booking_trend: List["BookingDataPoint"] = Field(default_factory=list)


class BookingDataPoint(BaseSchema):
    """Booking data point"""
    date: date
    total_bookings: int
    approved: int
    rejected: int


class ComplaintAnalytics(BaseSchema):
    """Complaint analytics"""
    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    closed_complaints: int
    
    average_resolution_time_hours: Decimal
    resolution_rate: Decimal = Field(..., description="% of resolved complaints")
    
    # By category
    complaints_by_category: Dict[str, int] = Field(default_factory=dict)
    
    # By priority
    complaints_by_priority: Dict[str, int] = Field(default_factory=dict)
    
    # SLA compliance
    sla_compliance_rate: Decimal = Field(..., description="% meeting SLA")


class ReviewAnalytics(BaseSchema):
    """Review analytics"""
    total_reviews: int
    average_rating: Decimal
    
    # Rating distribution
    rating_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of ratings by star (1-5)"
    )
    
    # Detailed ratings
    average_cleanliness_rating: Optional[Decimal] = None
    average_food_quality_rating: Optional[Decimal] = None
    average_staff_behavior_rating: Optional[Decimal] = None
    average_security_rating: Optional[Decimal] = None
    average_value_rating: Optional[Decimal] = None
    
    # Trends
    rating_trend: List["RatingDataPoint"] = Field(default_factory=list)


class RatingDataPoint(BaseSchema):
    """Rating data point"""
    month: str
    average_rating: Decimal
    review_count: int


class HostelOccupancyStats(BaseSchema):
    """Detailed occupancy statistics"""
    hostel_id: UUID
    
    # Current status
    total_rooms: int
    total_beds: int
    occupied_beds: int
    available_beds: int
    occupancy_percentage: Decimal
    
    # By room type
    occupancy_by_room_type: List["RoomTypeOccupancy"] = Field(default_factory=list)
    
    # Historical
    occupancy_history: List[OccupancyDataPoint] = Field(default_factory=list)
    
    # Projections
    projected_occupancy_30_days: Optional[Decimal] = None
    projected_occupancy_90_days: Optional[Decimal] = None


class RoomTypeOccupancy(BaseSchema):
    """Occupancy by room type"""
    room_type: str
    total_beds: int
    occupied_beds: int
    available_beds: int
    occupancy_percentage: Decimal


class HostelRevenueStats(BaseSchema):
    """Detailed revenue statistics"""
    hostel_id: UUID
    period: DateRangeFilter
    
    # Totals
    total_revenue: Decimal
    total_expenses: Decimal
    net_profit: Decimal
    profit_margin: Decimal
    
    # Revenue breakdown
    revenue_by_type: Dict[str, Decimal] = Field(default_factory=dict)
    
    # Collection
    total_collected: Decimal
    total_pending: Decimal
    total_overdue: Decimal
    collection_efficiency: Decimal
    
    # Monthly breakdown
    monthly_revenue: List["MonthlyRevenue"] = Field(default_factory=list)
    
    # Comparison
    revenue_growth_mom: Decimal = Field(..., description="Month-over-month growth %")
    revenue_growth_yoy: Optional[Decimal] = Field(None, description="Year-over-year growth %")


class MonthlyRevenue(BaseSchema):
    """Monthly revenue breakdown"""
    month: str  # YYYY-MM format
    revenue: Decimal
    collected: Decimal
    pending: Decimal
    student_count: int
    average_revenue_per_student: Decimal


class AnalyticsRequest(BaseSchema):
    """Analytics generation request"""
    hostel_id: UUID
    start_date: date
    end_date: date
    include_predictions: bool = Field(False, description="Include predictive analytics")
    granularity: str = Field("daily", pattern="^(daily|weekly|monthly)$")