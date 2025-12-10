"""
Complaint response schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import ComplaintCategory, ComplaintStatus, Priority


class ComplaintResponse(BaseResponseSchema):
    """Complaint response schema"""
    complaint_number: str
    hostel_id: UUID
    hostel_name: str
    
    raised_by: UUID
    raised_by_name: str
    student_id: Optional[UUID]
    
    title: str
    category: ComplaintCategory
    priority: Priority
    status: ComplaintStatus
    
    assigned_to: Optional[UUID]
    assigned_to_name: Optional[str]
    
    opened_at: datetime
    resolved_at: Optional[datetime]
    
    # SLA
    sla_breach: bool
    age_hours: int


class ComplaintDetail(BaseResponseSchema):
    """Detailed complaint information"""
    complaint_number: str
    
    # Hostel
    hostel_id: UUID
    hostel_name: str
    
    # Raised by
    raised_by: UUID
    raised_by_name: str
    raised_by_email: str
    raised_by_phone: str
    
    student_id: Optional[UUID]
    student_name: Optional[str]
    room_number: Optional[str]
    
    # Complaint details
    title: str
    description: str
    category: ComplaintCategory
    sub_category: Optional[str]
    priority: Priority
    
    # Location
    room_id: Optional[UUID]
    location_details: Optional[str]
    
    # Attachments
    attachments: List[str]
    
    # Assignment
    assigned_to: Optional[UUID]
    assigned_to_name: Optional[str]
    assigned_by: Optional[UUID]
    assigned_by_name: Optional[str]
    assigned_at: Optional[datetime]
    reassigned_count: int
    
    # Status workflow
    status: ComplaintStatus
    opened_at: datetime
    in_progress_at: Optional[datetime]
    resolved_at: Optional[datetime]
    closed_at: Optional[datetime]
    closed_by: Optional[UUID]
    closed_by_name: Optional[str]
    
    # Resolution
    resolution_notes: Optional[str]
    resolution_attachments: List[str]
    estimated_resolution_time: Optional[datetime]
    actual_resolution_time: Optional[datetime]
    
    # Feedback
    student_feedback: Optional[str]
    student_rating: Optional[int]
    feedback_submitted_at: Optional[datetime]
    
    # SLA
    sla_breach: bool
    sla_breach_reason: Optional[str]
    
    # Escalation
    escalated: bool
    escalated_to: Optional[UUID]
    escalated_to_name: Optional[str]
    escalated_at: Optional[datetime]
    escalation_reason: Optional[str]
    
    # Admin override
    overridden_by_admin: bool
    override_admin_id: Optional[UUID]
    override_timestamp: Optional[datetime]
    override_reason: Optional[str]
    
    # Comments count
    total_comments: int
    
    # Time tracking
    age_hours: int
    time_to_resolve_hours: Optional[int]


class ComplaintListItem(BaseSchema):
    """Complaint list item"""
    id: UUID
    complaint_number: str
    title: str
    
    category: str
    priority: str
    status: ComplaintStatus
    
    raised_by_name: str
    room_number: Optional[str]
    
    assigned_to_name: Optional[str]
    
    opened_at: datetime
    age_hours: int
    
    sla_breach: bool


class ComplaintSummary(BaseSchema):
    """Complaint summary for dashboard"""
    hostel_id: UUID
    
    total_complaints: int
    open_complaints: int
    in_progress_complaints: int
    resolved_complaints: int
    
    high_priority_count: int
    urgent_priority_count: int
    
    sla_breached_count: int
    
    average_resolution_time_hours: Decimal