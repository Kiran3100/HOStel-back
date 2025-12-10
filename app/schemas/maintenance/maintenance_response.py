"""
Maintenance response schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import MaintenanceCategory, MaintenanceStatus, Priority


class MaintenanceResponse(BaseResponseSchema):
    """Maintenance response schema"""
    request_number: str
    hostel_id: UUID
    hostel_name: str
    
    requested_by: UUID
    requested_by_name: str
    
    title: str
    category: MaintenanceCategory
    priority: Priority
    status: MaintenanceStatus
    
    assigned_to: Optional[UUID]
    assigned_to_name: Optional[str]
    
    estimated_cost: Optional[Decimal]
    actual_cost: Optional[Decimal]
    
    created_at: datetime
    estimated_completion_date: Optional[date]
    completed_at: Optional[datetime]


class MaintenanceDetail(BaseResponseSchema):
    """Detailed maintenance information"""
    request_number: str
    
    # Hostel
    hostel_id: UUID
    hostel_name: str
    
    # Requester
    requested_by: UUID
    requested_by_name: str
    room_id: Optional[UUID]
    room_number: Optional[str]
    
    # Request details
    title: str
    description: str
    category: MaintenanceCategory
    priority: Priority
    issue_type: str
    
    # Location
    location: Optional[str]
    floor: Optional[int]
    specific_area: Optional[str]
    
    # Photos
    issue_photos: List[str]
    completion_photos: List[str]
    
    # Assignment
    assigned_to: Optional[UUID]
    assigned_to_name: Optional[str]
    assigned_by: Optional[UUID]
    assigned_by_name: Optional[str]
    assigned_at: Optional[datetime]
    
    vendor_name: Optional[str]
    vendor_contact: Optional[str]
    
    # Status workflow
    status: MaintenanceStatus
    approved_by: Optional[UUID]
    approved_by_name: Optional[str]
    approved_at: Optional[datetime]
    
    rejected_by: Optional[UUID]
    rejected_at: Optional[datetime]
    rejection_reason: Optional[str]
    
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    # Cost
    estimated_cost: Optional[Decimal]
    actual_cost: Optional[Decimal]
    cost_approved: bool
    approval_threshold_exceeded: bool
    
    # Timeline
    estimated_completion_date: Optional[date]
    actual_completion_date: Optional[date]
    
    # Work details
    work_notes: Optional[str]
    materials_used: List[dict] = Field(default_factory=list)
    labor_hours: Optional[Decimal]
    
    # Quality check
    quality_checked_by: Optional[UUID]
    quality_check_passed: Optional[bool]
    quality_check_notes: Optional[str]
    quality_checked_at: Optional[datetime]
    
    # Preventive
    is_preventive: bool
    next_scheduled_date: Optional[date]
    recurrence: str


class RequestListItem(BaseSchema):
    """Maintenance request list item"""
    id: UUID
    request_number: str
    title: str
    
    category: str
    priority: str
    status: MaintenanceStatus
    
    room_number: Optional[str]
    
    estimated_cost: Optional[Decimal]
    
    assigned_to_name: Optional[str]
    
    created_at: datetime
    estimated_completion_date: Optional[date]


class MaintenanceSummary(BaseSchema):
    """Maintenance summary for hostel"""
    hostel_id: UUID
    
    total_requests: int
    pending_requests: int
    in_progress_requests: int
    completed_requests: int
    
    high_priority_count: int
    urgent_priority_count: int
    
    total_estimated_cost: Decimal
    total_actual_cost: Decimal
    
    average_completion_time_hours: Decimal