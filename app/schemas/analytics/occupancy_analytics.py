"""
Occupancy analytics schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Optional

from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class OccupancyKPI(BaseSchema):
    """Key occupancy metrics"""
    hostel_id: Optional[UUID] = None
    hostel_name: Optional[str] = None

    current_occupancy_percentage: Decimal
    average_occupancy_percentage: Decimal
    peak_occupancy_percentage: Decimal
    low_occupancy_percentage: Decimal

    total_beds: int
    occupied_beds: int
    available_beds: int


class OccupancyTrendPoint(BaseSchema):
    """Occupancy over time point"""
    date: date
    occupancy_percentage: Decimal
    occupied_beds: int
    total_beds: int


class ForecastData(BaseSchema):
    """Occupancy forecast data"""
    forecast_horizon_days: int
    forecast_points: List["ForecastPoint"] = Field(default_factory=list)
    model_used: Optional[str] = Field(
        None, description="e.g., 'moving_average', 'arima', 'simple_extrapolation'"
    )
    confidence_interval: Optional[Decimal] = Field(
        None, description="Confidence interval for forecast in %"
    )


class ForecastPoint(BaseSchema):
    """Single forecast point"""
    date: date
    forecasted_occupancy_percentage: Decimal
    forecasted_occupied_beds: int


class OccupancyByRoomType(BaseSchema):
    """Occupancy distribution by room type"""
    room_type: str
    total_beds: int
    occupied_beds: int
    occupancy_percentage: Decimal


class OccupancyReport(BaseSchema):
    """Complete occupancy analytics"""
    hostel_id: Optional[UUID] = None
    hostel_name: Optional[str] = None

    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    kpi: OccupancyKPI

    # Trends
    daily_trend: List[OccupancyTrendPoint] = Field(default_factory=list)

    # Breakdown
    by_room_type: List[OccupancyByRoomType] = Field(default_factory=list)
    by_floor: Dict[int, OccupancyKPI] = Field(default_factory=dict)

    # Forecast
    forecast: Optional[ForecastData] = None