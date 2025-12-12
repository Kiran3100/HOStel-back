"""
Complaint filter and search schemas with optimized query building.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import ComplaintCategory, ComplaintStatus, Priority


class ComplaintFilterParams(BaseFilterSchema):
    """Complaint filter parameters with validation."""
    
    # Text search
    search: Optional[str] = Field(None, max_length=255, description="Search in title, description, number")
    
    # Hostel filter
    hostel_id: Optional[UUID] = None
    hostel_ids: Optional[List[UUID]] = Field(None, max_items=50)
    
    # Raised by
    raised_by: Optional[UUID] = None
    student_id: Optional[UUID] = None
    
    # Assignment
    assigned_to: Optional[UUID] = None
    unassigned_only: Optional[bool] = None
    
    # Category
    category: Optional[ComplaintCategory] = None
    categories: Optional[List[ComplaintCategory]] = Field(None, max_items=10)
    
    # Priority
    priority: Optional[Priority] = None
    priorities: Optional[List[Priority]] = Field(None, max_items=5)
    
    # Status
    status: Optional[ComplaintStatus] = None
    statuses: Optional[List[ComplaintStatus]] = Field(None, max_items=7)
    
    # Date filters
    opened_date_from: Optional[date] = None
    opened_date_to: Optional[date] = None
    resolved_date_from: Optional[date] = None
    resolved_date_to: Optional[date] = None
    
    # SLA
    sla_breached_only: Optional[bool] = None
    
    # Escalation
    escalated_only: Optional[bool] = None
    
    # Room
    room_id: Optional[UUID] = None
    
    # Age
    age_hours_min: Optional[int] = Field(None, ge=0, le=8760)
    age_hours_max: Optional[int] = Field(None, ge=0, le=8760)

    @field_validator("search")
    @classmethod
    def normalize_search(cls, v: Optional[str]) -> Optional[str]:
        """Normalize search query."""
        if v:
            v = v.strip()
            if len(v) < 2:
                raise ValueError("Search query must be at least 2 characters")
        return v

    @model_validator(mode="after")
    def validate_date_ranges(self) -> "ComplaintFilterParams":
        """Validate date ranges are logical."""
        if self.opened_date_from and self.opened_date_to:
            if self.opened_date_from > self.opened_date_to:
                raise ValueError("opened_date_from must be before opened_date_to")
                
        if self.resolved_date_from and self.resolved_date_to:
            if self.resolved_date_from > self.resolved_date_to:
                raise ValueError("resolved_date_from must be before resolved_date_to")
                
        if self.age_hours_min and self.age_hours_max:
            if self.age_hours_min > self.age_hours_max:
                raise ValueError("age_hours_min must be less than age_hours_max")
                
        return self

    @model_validator(mode="after")
    def validate_list_filters(self) -> "ComplaintFilterParams":
        """Ensure single and list filters aren't both specified."""
        if self.category and self.categories:
            raise ValueError("Cannot specify both category and categories")
        if self.priority and self.priorities:
            raise ValueError("Cannot specify both priority and priorities")
        if self.status and self.statuses:
            raise ValueError("Cannot specify both status and statuses")
        if self.hostel_id and self.hostel_ids:
            raise ValueError("Cannot specify both hostel_id and hostel_ids")
        return self


class