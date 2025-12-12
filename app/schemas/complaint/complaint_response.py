"""
Complaint response schemas with enhanced factory methods and computed fields.
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import Field, computed_field

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import ComplaintCategory, ComplaintStatus, Priority


class ComplaintResponse(BaseResponseSchema):
    """Complaint response schema with computed fields."""
    
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

    @computed_field
    @property
    def is_overdue(self) -> bool:
        """Check if complaint is overdue based on priority."""
        if self.status in [ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED]:
            return False
            
        priority_sla_hours = {
            Priority.CRITICAL: 4,
            Priority.URGENT: 8,
            Priority.HIGH: 24,
            Priority.MEDIUM: 48,
            Priority.LOW: 72
        }
        
        return self.age_hours > priority_sla_hours.get(self.priority, 72)

    @computed_field
    @property
    def status_badge_color(self) -> str:
        """Get UI badge color for status."""
        status_colors = {
            ComplaintStatus.OPEN: "red",
            ComplaintStatus.ASSIGNED: "orange",
            ComplaintStatus.IN_PROGRESS: "yellow",
            ComplaintStatus.ON_HOLD: "gray",
            ComplaintStatus.RESOLVED: "green",
            ComplaintStatus.CLOSED: "blue",
            ComplaintStatus.REOPENED: "red"
        }
        return status_colors.get(self.status, "gray")


class ComplaintDetail(BaseResponseSchema):
    """Detailed complaint information with all relationships."""
    
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
    reassigned_count: int = Field(default=0, ge=0)
    
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
    resolution_attachments: List[str] = Field(default_factory=list)
    estimated_resolution_time: Optional[datetime]
    actual_resolution_time: Optional[datetime]
    
    # Feedback
    student_feedback: Optional[str]
    student_rating: Optional[int] = Field(None, ge=1, le=5)
    feedback_submitted_at: Optional[datetime]
    
    # SLA
    sla_breach: bool = Field(default=False)
    sla_breach_reason: Optional[str]
    
    # Escalation
    escalated: bool = Field(default=False)
    escalated_to: Optional[UUID]
    escalated_to_name: Optional[str]
    escalated_at: Optional[datetime]
    escalation_reason: Optional[str]
    
    # Admin override
    overridden_by_admin: bool = Field(default=False)
    override_admin_id: Optional[UUID]
    override_timestamp: Optional[datetime]
    override_reason: Optional[str]
    
    # Comments count
    total_comments: int = Field(default=0, ge=0)
    
    # Time tracking
    age_hours: int = Field(..., ge=0)
    time_to_resolve_hours: Optional[int] = Field(None, ge=0)

    @computed_field
    @property
    def resolution_efficiency(self) -> Optional[str]:
        """Calculate resolution efficiency rating."""
        if not self.time_to_resolve_hours:
            return None
            
        priority_targets = {
            Priority.CRITICAL: 4,
            Priority.URGENT: 8,
            Priority.HIGH: 24,
            Priority.MEDIUM: 48,
            Priority.LOW: 72
        }
        
        target = priority_targets.get(self.priority, 72)
        
        if self.time_to_resolve_hours <= target * 0.5:
            return "excellent"
        elif self.time_to_resolve_hours <= target:
            return "good"
        elif self.time_to_resolve_hours <= target * 1.5:
            return "fair"
        else:
            return "poor"


class ComplaintListItem(BaseSchema):
    """Optimized complaint list item for performance."""
    
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

    @computed_field
    @property
    def priority_icon(self) -> str:
        """Get icon identifier for priority."""
        priority_icons = {
            "critical": "🔴",
            "urgent": "🟠",
            "high": "🟡",
            "medium": "🟢",
            "low": "🔵"
        }
        return priority_icons.get(self.priority.lower(), "⚪")

    class Config:
        # Optimize for list serialization
        validate_assignment = False


class ComplaintSummary(BaseSchema):
    """Complaint summary for dashboard with calculated metrics."""
    
    hostel_id: UUID
    
    total_complaints: int = Field(..., ge=0)
    open_complaints: int = Field(..., ge=0)
    in_progress_complaints: int = Field(..., ge=0)
    resolved_complaints: int = Field(..., ge=0)
    
    high_priority_count: int = Field(..., ge=0)
    urgent_priority_count: int = Field(..., ge=0)
    
    sla_breached_count: int = Field(..., ge=0)
    
    average_resolution_time_hours: Decimal = Field(..., ge=0)

    @computed_field
    @property
    def resolution_rate(self) -> Decimal:
        """Calculate resolution rate percentage."""
        if self.total_complaints == 0:
            return Decimal("0")
        return Decimal(self.resolved_complaints * 100) / Decimal(self.total_complaints)

    @computed_field
    @property
    def sla_compliance_rate(self) -> Decimal:
        """Calculate SLA compliance rate percentage."""
        if self.total_complaints == 0:
            return Decimal("100")
        compliant = self.total_complaints - self.sla_breached_count
        return Decimal(compliant * 100) / Decimal(self.total_complaints)