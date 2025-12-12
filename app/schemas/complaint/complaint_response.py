"""
Complaint response schemas for API outputs.

Provides comprehensive response models for different complaint views:
- Summary responses for list views
- Detailed responses for single complaint views
- Dashboard summary statistics
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import Field, computed_field

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import ComplaintCategory, ComplaintStatus, Priority

__all__ = [
    "ComplaintResponse",
    "ComplaintDetail",
    "ComplaintListItem",
    "ComplaintSummary",
    "ComplaintStats",
]


class ComplaintResponse(BaseResponseSchema):
    """
    Standard complaint response with essential fields.
    
    Used for list views and general complaint information.
    """

    complaint_number: str = Field(
        ...,
        description="Unique complaint reference number",
    )
    hostel_id: str = Field(
        ...,
        description="Associated hostel identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Associated hostel name for display",
    )

    # Complainant information
    raised_by: str = Field(
        ...,
        description="User ID who raised the complaint",
    )
    raised_by_name: str = Field(
        ...,
        description="Display name of complainant",
    )
    student_id: Optional[str] = Field(
        None,
        description="Student ID if applicable",
    )

    # Core complaint fields
    title: str = Field(
        ...,
        description="Complaint title",
    )
    category: ComplaintCategory = Field(
        ...,
        description="Complaint category",
    )
    priority: Priority = Field(
        ...,
        description="Priority level",
    )
    status: ComplaintStatus = Field(
        ...,
        description="Current status",
    )

    # Assignment
    assigned_to: Optional[str] = Field(
        None,
        description="Assigned staff member ID",
    )
    assigned_to_name: Optional[str] = Field(
        None,
        description="Assigned staff member name",
    )

    # Timestamps
    opened_at: datetime = Field(
        ...,
        description="Complaint creation timestamp",
    )
    resolved_at: Optional[datetime] = Field(
        None,
        description="Resolution timestamp",
    )

    # Metrics
    sla_breach: bool = Field(
        ...,
        description="Whether complaint has breached SLA",
    )
    age_hours: int = Field(
        ...,
        ge=0,
        description="Age of complaint in hours",
    )

    @computed_field
    @property
    def is_overdue(self) -> bool:
        """Determine if complaint is overdue based on priority and age."""
        # Define SLA thresholds in hours by priority
        sla_thresholds = {
            Priority.CRITICAL: 2,
            Priority.URGENT: 4,
            Priority.HIGH: 12,
            Priority.MEDIUM: 24,
            Priority.LOW: 48,
        }
        
        threshold = sla_thresholds.get(self.priority, 24)
        return self.age_hours > threshold and self.status not in [
            ComplaintStatus.RESOLVED,
            ComplaintStatus.CLOSED,
        ]


class ComplaintDetail(BaseResponseSchema):
    """
    Comprehensive complaint details with full information.
    
    Used for single complaint view with complete audit trail
    and relationship information.
    """

    complaint_number: str = Field(
        ...,
        description="Unique complaint reference number",
    )

    # Hostel information
    hostel_id: str = Field(..., description="Hostel identifier")
    hostel_name: str = Field(..., description="Hostel name")

    # Complainant information (detailed)
    raised_by: str = Field(..., description="User ID of complainant")
    raised_by_name: str = Field(..., description="Complainant name")
    raised_by_email: str = Field(..., description="Complainant email")
    raised_by_phone: str = Field(..., description="Complainant phone")

    student_id: Optional[str] = Field(None, description="Student ID")
    student_name: Optional[str] = Field(None, description="Student name")
    room_number: Optional[str] = Field(None, description="Room number")

    # Complaint content
    title: str = Field(..., description="Complaint title")
    description: str = Field(..., description="Detailed description")
    category: ComplaintCategory = Field(..., description="Category")
    sub_category: Optional[str] = Field(None, description="Sub-category")
    priority: Priority = Field(..., description="Priority level")

    # Location
    room_id: Optional[str] = Field(None, description="Room ID")
    location_details: Optional[str] = Field(None, description="Location details")

    # Media
    attachments: List[str] = Field(
        default_factory=list,
        description="Attachment URLs",
    )

    # Assignment history
    assigned_to: Optional[str] = Field(None, description="Current assignee ID")
    assigned_to_name: Optional[str] = Field(None, description="Current assignee name")
    assigned_by: Optional[str] = Field(None, description="Assigned by user ID")
    assigned_by_name: Optional[str] = Field(None, description="Assigned by name")
    assigned_at: Optional[datetime] = Field(None, description="Assignment timestamp")
    reassigned_count: int = Field(
        default=0,
        ge=0,
        description="Number of times complaint was reassigned",
    )

    # Status workflow
    status: ComplaintStatus = Field(..., description="Current status")
    opened_at: datetime = Field(..., description="Creation timestamp")
    in_progress_at: Optional[datetime] = Field(
        None,
        description="When complaint moved to in-progress",
    )
    resolved_at: Optional[datetime] = Field(
        None,
        description="Resolution timestamp",
    )
    closed_at: Optional[datetime] = Field(None, description="Closure timestamp")
    closed_by: Optional[str] = Field(None, description="User who closed complaint")
    closed_by_name: Optional[str] = Field(None, description="Closer name")

    # Resolution details
    resolution_notes: Optional[str] = Field(
        None,
        description="Resolution description",
    )
    resolution_attachments: List[str] = Field(
        default_factory=list,
        description="Resolution proof URLs",
    )
    estimated_resolution_time: Optional[datetime] = Field(
        None,
        description="Estimated resolution time",
    )
    actual_resolution_time: Optional[datetime] = Field(
        None,
        description="Actual resolution time",
    )

    # Feedback
    student_feedback: Optional[str] = Field(None, description="Student feedback")
    student_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Student rating (1-5)",
    )
    feedback_submitted_at: Optional[datetime] = Field(
        None,
        description="Feedback submission timestamp",
    )

    # SLA tracking
    sla_breach: bool = Field(..., description="SLA breach status")
    sla_breach_reason: Optional[str] = Field(
        None,
        description="Reason for SLA breach",
    )

    # Escalation
    escalated: bool = Field(default=False, description="Escalation status")
    escalated_to: Optional[str] = Field(None, description="Escalated to user ID")
    escalated_to_name: Optional[str] = Field(None, description="Escalated to name")
    escalated_at: Optional[datetime] = Field(None, description="Escalation timestamp")
    escalation_reason: Optional[str] = Field(None, description="Escalation reason")

    # Admin override
    overridden_by_admin: bool = Field(
        default=False,
        description="Admin override flag",
    )
    override_admin_id: Optional[str] = Field(None, description="Override admin ID")
    override_timestamp: Optional[datetime] = Field(
        None,
        description="Override timestamp",
    )
    override_reason: Optional[str] = Field(None, description="Override reason")

    # Engagement metrics
    total_comments: int = Field(
        default=0,
        ge=0,
        description="Total comment count",
    )

    # Time metrics
    age_hours: int = Field(ge=0, description="Complaint age in hours")
    time_to_resolve_hours: Optional[int] = Field(
        None,
        ge=0,
        description="Time taken to resolve (hours)",
    )

    @computed_field
    @property
    def is_active(self) -> bool:
        """Check if complaint is in an active state."""
        active_statuses = {
            ComplaintStatus.OPEN,
            ComplaintStatus.ASSIGNED,
            ComplaintStatus.IN_PROGRESS,
            ComplaintStatus.REOPENED,
        }
        return self.status in active_statuses

    @computed_field
    @property
    def resolution_efficiency(self) -> Optional[str]:
        """
        Calculate resolution efficiency rating.
        
        Returns:
            Efficiency rating: 'excellent', 'good', 'average', 'poor', or None
        """
        if not self.time_to_resolve_hours:
            return None
        
        # Define efficiency thresholds based on priority
        thresholds = {
            Priority.CRITICAL: {"excellent": 1, "good": 2, "average": 4},
            Priority.URGENT: {"excellent": 2, "good": 4, "average": 8},
            Priority.HIGH: {"excellent": 6, "good": 12, "average": 24},
            Priority.MEDIUM: {"excellent": 12, "good": 24, "average": 48},
            Priority.LOW: {"excellent": 24, "good": 48, "average": 72},
        }
        
        threshold = thresholds.get(self.priority, thresholds[Priority.MEDIUM])
        hours = self.time_to_resolve_hours
        
        if hours <= threshold["excellent"]:
            return "excellent"
        elif hours <= threshold["good"]:
            return "good"
        elif hours <= threshold["average"]:
            return "average"
        else:
            return "poor"


class ComplaintListItem(BaseSchema):
    """
    Lightweight complaint item for list views.
    
    Optimized for performance with minimal fields
    for table/grid displays.
    """

    id: str = Field(..., description="Complaint ID")
    complaint_number: str = Field(..., description="Reference number")
    title: str = Field(..., description="Complaint title")

    category: str = Field(..., description="Category name")
    priority: str = Field(..., description="Priority level")
    status: ComplaintStatus = Field(..., description="Current status")

    raised_by_name: str = Field(..., description="Complainant name")
    room_number: Optional[str] = Field(None, description="Room number")

    assigned_to_name: Optional[str] = Field(None, description="Assignee name")

    opened_at: datetime = Field(..., description="Creation timestamp")
    age_hours: int = Field(ge=0, description="Age in hours")

    sla_breach: bool = Field(..., description="SLA breach status")

    @computed_field
    @property
    def status_color(self) -> str:
        """
        Get status color code for UI display.
        
        Returns:
            Color code string for status badge
        """
        color_map = {
            ComplaintStatus.OPEN: "red",
            ComplaintStatus.ASSIGNED: "orange",
            ComplaintStatus.IN_PROGRESS: "blue",
            ComplaintStatus.ON_HOLD: "yellow",
            ComplaintStatus.RESOLVED: "green",
            ComplaintStatus.CLOSED: "gray",
            ComplaintStatus.REOPENED: "purple",
        }
        return color_map.get(self.status, "gray")

    @computed_field
    @property
    def priority_weight(self) -> int:
        """
        Get numeric priority weight for sorting.
        
        Returns:
            Integer weight (higher = more urgent)
        """
        weight_map = {
            "critical": 5,
            "urgent": 4,
            "high": 3,
            "medium": 2,
            "low": 1,
        }
        return weight_map.get(self.priority.lower(), 2)


class ComplaintSummary(BaseSchema):
    """
    Complaint statistics summary for dashboard.
    
    Provides aggregate metrics for a hostel or supervisor.
    """

    hostel_id: str = Field(..., description="Hostel identifier")

    total_complaints: int = Field(ge=0, description="Total complaint count")
    open_complaints: int = Field(ge=0, description="Open complaints")
    in_progress_complaints: int = Field(ge=0, description="In-progress complaints")
    resolved_complaints: int = Field(ge=0, description="Resolved complaints")

    high_priority_count: int = Field(ge=0, description="High priority count")
    urgent_priority_count: int = Field(ge=0, description="Urgent priority count")

    sla_breached_count: int = Field(ge=0, description="SLA breached count")

    average_resolution_time_hours: Decimal = Field(
        ge=0,
        description="Average resolution time in hours",
    )

    @computed_field
    @property
    def resolution_rate(self) -> float:
        """
        Calculate complaint resolution rate percentage.
        
        Returns:
            Resolution rate as percentage (0-100)
        """
        if self.total_complaints == 0:
            return 0.0
        return round(
            (self.resolved_complaints / self.total_complaints) * 100,
            2
        )

    @computed_field
    @property
    def sla_compliance_rate(self) -> float:
        """
        Calculate SLA compliance rate percentage.
        
        Returns:
            SLA compliance rate as percentage (0-100)
        """
        if self.total_complaints == 0:
            return 100.0
        
        compliant = self.total_complaints - self.sla_breached_count
        return round((compliant / self.total_complaints) * 100, 2)


class ComplaintStats(BaseSchema):
    """
    Extended complaint statistics with breakdown details.
    
    Provides comprehensive analytics for reporting.
    """

    total: int = Field(ge=0, description="Total complaints")
    
    # Status breakdown
    by_status: dict[str, int] = Field(
        default_factory=dict,
        description="Complaint count by status",
    )
    
    # Priority breakdown
    by_priority: dict[str, int] = Field(
        default_factory=dict,
        description="Complaint count by priority",
    )
    
    # Category breakdown
    by_category: dict[str, int] = Field(
        default_factory=dict,
        description="Complaint count by category",
    )
    
    # Time-based metrics
    avg_resolution_hours: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Average resolution time",
    )
    median_resolution_hours: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Median resolution time",
    )
    
    # Performance indicators
    sla_compliance_percentage: Decimal = Field(
        ge=0,
        le=100,
        description="SLA compliance percentage",
    )
    resolution_percentage: Decimal = Field(
        ge=0,
        le=100,
        description="Resolution percentage",
    )