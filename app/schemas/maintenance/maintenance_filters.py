"""
Maintenance filter schemas
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import MaintenanceCategory, MaintenanceStatus, Priority


class MaintenanceFilterParams(BaseFilterSchema):
    """Maintenance filter parameters"""
    # Text search
    search: Optional[str] = Field(None, description="Search in title, description, request number")
    
    # Hostel filter
    hostel_id: Optional[UUID] = None
    hostel_ids: Optional[List[UUID]] = None
    
    # Requested by
    requested_by: Optional[UUID] = None
    
    # Assignment
    assigned_to: Optional[UUID] = None
    unassigned_only: Optional[bool] = None
    
    # Room
    room_id: Optional[UUID] = None
    
    # Category
    category: Optional[MaintenanceCategory] = None
    categories: Optional[List[MaintenanceCategory]] = None
    
    # Priority
    priority: Optional[Priority] = None
    priorities: Optional[List[Priority]] = None
    
    # Status
    status: Optional[MaintenanceStatus] = None
    statuses: Optional[List[MaintenanceStatus]] = None
    
    # Date filters
    created_date_from: Optional[date] = None
    created_date_to: Optional[date] = None
    completion_date_from: Optional[date] = None
    completion_date_to: Optional[date] = None
    
    # Cost filters
    estimated_cost_min: Optional[Decimal] = None
    estimated_cost_max: Optional[Decimal] = None
    actual_cost_min: Optional[Decimal] = None
    actual_cost_max: Optional[Decimal] = None
    
    # Approval
    approval_pending: Optional[bool] = None
    
    # Preventive
    is_preventive: Optional[bool] = None


class SearchRequest(BaseFilterSchema):
    """Maintenance search request"""
    query: str = Field(..., min_length=1)
    hostel_id: Optional[UUID] = None
    
    search_in_title: bool = Field(True)
    search_in_description: bool = Field(True)
    search_in_number: bool = Field(True)
    
    status: Optional[MaintenanceStatus] = None
    
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class MaintenanceExportRequest(BaseFilterSchema):
    """Export maintenance data"""
    hostel_id: Optional[UUID] = None
    filters: Optional[MaintenanceFilterParams] = None
    
    format: str = Field("csv", pattern="^(csv|excel|pdf)$")
    
    include_cost_details: bool = Field(True)
    include_assignment_details: bool = Field(True)
    include_completion_details: bool = Field(True)