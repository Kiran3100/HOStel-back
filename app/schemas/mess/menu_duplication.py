"""
Menu duplication schemas
"""
from datetime import date
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class DuplicateMenuRequest(BaseCreateSchema):
    """Duplicate menu to another date"""
    source_menu_id: UUID = Field(..., description="Menu to duplicate")
    target_date: date = Field(..., description="Date for duplicated menu")
    
    # Modifications
    modify_items: bool = Field(False, description="Allow modifications during duplication")
    modifications: Optional[dict] = None


class BulkMenuCreate(BaseCreateSchema):
    """Create menus for multiple dates using template"""
    hostel_id: UUID
    
    # Date range
    start_date: date
    end_date: date
    
    # Source
    source_type: str = Field(..., pattern="^(template|existing_menu|weekly_pattern)$")
    
    # If using template
    template_id: Optional[UUID] = None
    
    # If using existing menu
    source_menu_id: Optional[UUID] = None
    
    # If using weekly pattern
    weekly_pattern: Optional[dict] = Field(
        None,
        description="Day of week -> menu items mapping"
    )
    
    # Options
    skip_existing: bool = Field(True, description="Skip dates that already have menus")
    override_existing: bool = Field(False, description="Override existing menus")


class DuplicateResponse(BaseSchema):
    """Duplication response"""
    source_menu_id: UUID
    created_menus: List[UUID]
    
    total_created: int
    skipped: int
    
    message: str


class CrossHostelDuplication(BaseCreateSchema):
    """Duplicate menu to other hostels"""
    source_menu_id: UUID
    source_hostel_id: UUID
    
    target_hostel_ids: List[UUID] = Field(..., min_items=1)
    target_date: date
    
    # Adjust for hostel-specific preferences
    adapt_to_hostel_preferences: bool = Field(True)