"""
Complaint filter and search schemas
"""
from datetime import date, datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import ComplaintCategory, ComplaintStatus, Priority


class ComplaintFilterParams(BaseFilterSchema):
    """Complaint filter parameters"""
    # Text search
    search: Optional[str] = Field(None, description="Search in title, description, number")
    
    # Hostel filter
    hostel_id: Optional[UUID] = None
    hostel_ids: Optional[List[UUID]] = None
    
    # Raised by
    raised_by: Optional[UUID] = None
    student_id: Optional[UUID] = None
    
    # Assignment
    assigned_to: Optional[UUID] = None
    unassigned_only: Optional[bool] = None
    
    # Category
    category: Optional[ComplaintCategory] = None
    categories: Optional[List[ComplaintCategory]] = None
    
    # Priority
    priority: Optional[Priority] = None
    priorities: Optional[List[Priority]] = None
    
    # Status
    status: Optional[ComplaintStatus] = None
    statuses: Optional[List[ComplaintStatus]] = None
    
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
    age_hours_min: Optional[int] = Field(None, ge=0)
    age_hours_max: Optional[int] = Field(None, ge=0)


class ComplaintSearchRequest(BaseFilterSchema):
    """Complaint search request"""
    query: str = Field(..., min_length=1, description="Search query")
    hostel_id: Optional[UUID] = None
    
    # Search fields
    search_in_title: bool = Field(True)
    search_in_description: bool = Field(True)
    search_in_number: bool = Field(True)
    
    # Filters
    status: Optional[ComplaintStatus] = None
    priority: Optional[Priority] = None
    
    # Pagination
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class ComplaintSortOptions(BaseFilterSchema):
    """Complaint sorting options"""
    sort_by: str = Field(
        "opened_at",
        pattern="^(opened_at|priority|status|category|age)$"
    )
    sort_order: str = Field("desc", pattern="^(asc|desc)$")


class ComplaintExportRequest(BaseFilterSchema):
    """Export complaints"""
    hostel_id: Optional[UUID] = None
    filters: Optional[ComplaintFilterParams] = None
    
    format: str = Field("csv", pattern="^(csv|excel|pdf)$")
    
    # Fields to include
    include_comments: bool = Field(False)
    include_resolution_details: bool = Field(True)
    include_feedback: bool = Field(True)