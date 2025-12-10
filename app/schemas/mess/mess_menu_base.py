"""
Mess menu base schemas
"""
from datetime import date, time
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema


class MessMenuBase(BaseSchema):
    """Base mess menu schema"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    menu_date: date = Field(..., description="Menu date")
    day_of_week: str = Field(..., description="Day of week")
    
    # Meals
    breakfast_items: List[str] = Field(default_factory=list, description="Breakfast items")
    lunch_items: List[str] = Field(default_factory=list, description="Lunch items")
    snacks_items: List[str] = Field(default_factory=list, description="Snacks items")
    dinner_items: List[str] = Field(default_factory=list, description="Dinner items")
    
    # Timings
    breakfast_time: Optional[time] = Field(None, description="Breakfast serving time")
    lunch_time: Optional[time] = Field(None, description="Lunch serving time")
    snacks_time: Optional[time] = Field(None, description="Snacks serving time")
    dinner_time: Optional[time] = Field(None, description="Dinner serving time")
    
    # Special
    is_special_menu: bool = Field(False, description="Special occasion menu")
    special_occasion: Optional[str] = Field(None, max_length=255, description="Occasion name")
    
    # Dietary options
    vegetarian_available: bool = Field(True)
    non_vegetarian_available: bool = Field(False)
    vegan_available: bool = Field(False)
    jain_available: bool = Field(False)


class MessMenuCreate(MessMenuBase, BaseCreateSchema):
    """Create mess menu"""
    created_by: UUID = Field(..., description="Supervisor/Admin who created")


class MessMenuUpdate(BaseUpdateSchema):
    """Update mess menu"""
    breakfast_items: Optional[List[str]] = None
    lunch_items: Optional[List[str]] = None
    snacks_items: Optional[List[str]] = None
    dinner_items: Optional[List[str]] = None
    
    breakfast_time: Optional[time] = None
    lunch_time: Optional[time] = None
    snacks_time: Optional[time] = None
    dinner_time: Optional[time] = None
    
    is_special_menu: Optional[bool] = None
    special_occasion: Optional[str] = None
    
    vegetarian_available: Optional[bool] = None
    non_vegetarian_available: Optional[bool] = None