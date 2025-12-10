"""
Menu planning schemas
"""
from datetime import date
from typing import List, Optional, Dict
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class MenuPlanRequest(BaseCreateSchema):
    """Request to create menu plan"""
    hostel_id: UUID
    
    # Planning period
    start_date: date
    end_date: date
    
    # Template to use (if any)
    use_template: bool = Field(False)
    template_id: Optional[UUID] = None
    
    # Variety preferences
    ensure_variety: bool = Field(True, description="Avoid repeating items too often")
    min_days_between_repeat: int = Field(3, ge=1, le=7)
    
    # Dietary requirements
    vegetarian_days_per_week: int = Field(7, ge=0, le=7)
    
    # Budget
    target_cost_per_day: Optional[Decimal] = None


class WeeklyPlan(BaseCreateSchema):
    """Weekly menu plan"""
    hostel_id: UUID
    week_start_date: date
    
    # Daily menus
    monday: "DailyMenuPlan"
    tuesday: "DailyMenuPlan"
    wednesday: "DailyMenuPlan"
    thursday: "DailyMenuPlan"
    friday: "DailyMenuPlan"
    saturday: "DailyMenuPlan"
    sunday: "DailyMenuPlan"
    
    # Metadata
    created_by: UUID
    notes: Optional[str] = None


class DailyMenuPlan(BaseSchema):
    """Daily menu plan"""
    breakfast: List[str]
    lunch: List[str]
    snacks: List[str]
    dinner: List[str]
    
    is_special: bool = Field(False)
    special_occasion: Optional[str] = None


class MonthlyPlan(BaseCreateSchema):
    """Monthly menu plan"""
    hostel_id: UUID
    month: str  # YYYY-MM format
    
    # Weekly plans
    weeks: List[WeeklyPlan]
    
    # Special days
    special_days: List["SpecialDayMenu"] = Field(default_factory=list)


class SpecialMenu(BaseCreateSchema):
    """Special occasion menu"""
    hostel_id: UUID
    occasion_date: date
    occasion_name: str = Field(..., min_length=3, max_length=255)
    
    # Enhanced menu
    breakfast: List[str]
    lunch: List[str]
    snacks: List[str]
    dinner: List[str]
    
    # Additional items
    special_items: List[str] = Field(default_factory=list, description="Extra special items")
    
    # Budget
    budget: Optional[Decimal] = None


class SpecialDayMenu(BaseSchema):
    """Special day in monthly plan"""
    date: date
    occasion: str
    menu: DailyMenuPlan


class MenuTemplate(BaseCreateSchema):
    """Reusable menu template"""
    hostel_id: UUID
    template_name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    
    # Template type
    template_type: str = Field(..., pattern="^(weekly|festival|summer|winter)$")
    
    # Menu structure
    daily_menus: Dict[str, DailyMenuPlan] = Field(
        ...,
        description="Day name -> menu plan"
    )


class MenuSuggestion(BaseSchema):
    """AI/System generated menu suggestions"""
    hostel_id: UUID
    date: date
    
    suggested_breakfast: List[str]
    suggested_lunch: List[str]
    suggested_dinner: List[str]
    
    reason: str = Field(..., description="Why these items are suggested")
    
    # Scores
    variety_score: Decimal = Field(..., ge=0, le=10)
    nutrition_score: Decimal = Field(..., ge=0, le=10)
    cost_score: Decimal = Field(..., ge=0, le=10)