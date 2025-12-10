"""
Mess menu response schemas
"""
from datetime import date, time, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema


class MenuResponse(BaseResponseSchema):
    """Mess menu response"""
    hostel_id: UUID
    hostel_name: str
    menu_date: date
    day_of_week: str
    
    breakfast_items: List[str]
    lunch_items: List[str]
    snacks_items: List[str]
    dinner_items: List[str]
    
    is_special_menu: bool
    special_occasion: Optional[str]
    
    is_published: bool
    average_rating: Decimal


class MenuDetail(BaseResponseSchema):
    """Detailed menu information"""
    hostel_id: UUID
    hostel_name: str
    menu_date: date
    day_of_week: str
    
    # Meals with timings
    breakfast_items: List[str]
    breakfast_time: Optional[time]
    
    lunch_items: List[str]
    lunch_time: Optional[time]
    
    snacks_items: List[str]
    snacks_time: Optional[time]
    
    dinner_items: List[str]
    dinner_time: Optional[time]
    
    # Dietary options
    vegetarian_available: bool
    non_vegetarian_available: bool
    vegan_available: bool
    jain_available: bool
    
    # Special
    is_special_menu: bool
    special_occasion: Optional[str]
    
    # Management
    created_by: UUID
    created_by_name: str
    approved_by: Optional[UUID]
    approved_by_name: Optional[str]
    approved_at: Optional[datetime]
    
    is_published: bool
    published_at: Optional[datetime]
    
    # Feedback
    average_rating: Decimal
    total_feedback_count: int


class WeeklyMenu(BaseSchema):
    """Weekly menu display"""
    hostel_id: UUID
    hostel_name: str
    week_start_date: date
    week_end_date: date
    
    menus: List["DailyMenuSummary"]


class DailyMenuSummary(BaseSchema):
    """Daily menu summary for weekly view"""
    menu_id: UUID
    date: date
    day_of_week: str
    
    breakfast: List[str]
    lunch: List[str]
    dinner: List[str]
    
    is_special: bool
    average_rating: Optional[Decimal]


class MonthlyMenu(BaseSchema):
    """Monthly menu calendar"""
    hostel_id: UUID
    hostel_name: str
    month: str  # YYYY-MM format
    
    menus_by_date: dict = Field(..., description="Date -> DailyMenuSummary")
    
    # Summary
    total_days: int
    special_days: int
    average_rating: Decimal


class TodayMenu(BaseSchema):
    """Today's menu for student view"""
    hostel_id: UUID
    hostel_name: str
    date: date
    day_of_week: str
    
    breakfast: List[str]
    breakfast_time: str
    
    lunch: List[str]
    lunch_time: str
    
    snacks: List[str]
    snacks_time: str
    
    dinner: List[str]
    dinner_time: str
    
    is_special: bool
    special_occasion: Optional[str]
    
    dietary_note: Optional[str]