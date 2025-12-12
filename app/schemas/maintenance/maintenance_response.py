# --- File: app/schemas/maintenance/maintenance_response.py ---
"""
Maintenance response schemas for API responses.

Provides various response formats for maintenance data including
detailed, summary, and list views with computed fields.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import Field, computed_field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import (
    MaintenanceCategory,
    MaintenanceIssueType,
    MaintenanceStatus,
    Priority,
)

__all__ = [
    "MaintenanceResponse",
    "MaintenanceDetail",
    "RequestListItem",
    "MaintenanceSummary",
]


class MaintenanceResponse(BaseResponseSchema):
    """
    Standard maintenance response with essential information.
    
    Lightweight response schema for list views and basic queries.
    """

    request_number: str = Field(
        ...,
        description="Human-readable request number",
    )
    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )
    requested_by: UUID = Field(
        ...,
        description="Requester user ID",
    )
    requested_by_name: str = Field(
        ...,
        description="Requester full name",
    )
    title: str = Field(
        ...,
        description="Issue title",
    )
    category: MaintenanceCategory = Field(
        ...,
        description="Maintenance category",
    )
    priority: Priority = Field(
        ...,
        description="Issue priority",
    )
    status: MaintenanceStatus = Field(
        ...,
        description="Current status",
    )
    assigned_to: Optional[UUID] = Field(
        None,
        description="Assignee user ID",
    )
    assigned_to_name: Optional[str] = Field(
        None,
        description="Assignee name",
    )
    estimated_cost: Optional[Decimal] = Field(
        None,
        description="Estimated cost",
    )
    actual_cost: Optional[Decimal] = Field(
        None,
        description="Actual cost",
    )
    created_at: datetime = Field(
        ...,
        description="Request creation timestamp",
    )
    estimated_completion_date: Optional[date] = Field(
        None,
        description="Estimated completion date",
    )
    completed_at: Optional[datetime] = Field(
        None,
        description="Completion timestamp",
    )

    @computed_field
    @property
    def status_display(self) -> str:
        """Human-readable status display."""
        status_map = {
            MaintenanceStatus.PENDING: "Pending",
            MaintenanceStatus.APPROVED: "Approved",
            MaintenanceStatus.ASSIGNED: "Assigned",
            MaintenanceStatus.IN_PROGRESS: "In Progress",
            MaintenanceStatus.ON_HOLD: "On Hold",
            MaintenanceStatus.COMPLETED: "Completed",
            MaintenanceStatus.REJECTED: "Rejected",
            MaintenanceStatus.CANCELLED: "Cancelled",
        }
        return status_map.get(self.status, self.status.value)

    @computed_field
    @property
    def priority_display(self) -> str:
        """Human-readable priority display."""
        priority_map = {
            Priority.LOW: "Low",
            Priority.MEDIUM: "Medium",
            Priority.HIGH: "High",
            Priority.URGENT: "Urgent",
            Priority.CRITICAL: "Critical",
        }
        return priority_map.get(self.priority, self.priority.value)

    @computed_field
    @property
    def is_overdue(self) -> bool:
        """Check if request is overdue."""
        if not self.estimated_completion_date:
            return False
        
        if self.status == MaintenanceStatus.COMPLETED:
            return False
        
        return self.estimated_completion_date < date.today()

    @computed_field
    @property
    def days_since_creation(self) -> int:
        """Calculate days since request was created."""
        return (datetime.now() - self.created_at).days


class MaintenanceDetail(BaseResponseSchema):
    """
    Detailed maintenance information with complete metadata.
    
    Comprehensive response including all maintenance details, workflow,
    and supporting information.
    """

    request_number: str = Field(
        ...,
        description="Request number",
    )
    
    # Hostel information
    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )
    
    # Requester information
    requested_by: UUID = Field(
        ...,
        description="Requester user ID",
    )
    requested_by_name: str = Field(
        ...,
        description="Requester full name",
    )
    requested_by_email: Optional[str] = Field(
        None,
        description="Requester email",
    )
    requested_by_phone: Optional[str] = Field(
        None,
        description="Requester phone",
    )
    room_id: Optional[UUID] = Field(
        None,
        description="Room ID",
    )
    room_number: Optional[str] = Field(
        None,
        description="Room number",
    )
    
    # Request details
    title: str = Field(
        ...,
        description="Issue title",
    )
    description: str = Field(
        ...,
        description="Detailed description",
    )
    category: MaintenanceCategory = Field(
        ...,
        description="Maintenance category",
    )
    priority: Priority = Field(
        ...,
        description="Priority level",
    )
    issue_type: MaintenanceIssueType = Field(
        ...,
        description="Issue type",
    )
    
    # Location details
    location: Optional[str] = Field(
        None,
        description="Location details",
    )
    floor: Optional[int] = Field(
        None,
        description="Floor number",
    )
    specific_area: Optional[str] = Field(
        None,
        description="Specific area",
    )
    
    # Photos and documents
    issue_photos: List[str] = Field(
        default_factory=list,
        description="Issue photographs",
    )
    completion_photos: List[str] = Field(
        default_factory=list,
        description="Completion photographs",
    )
    
    # Assignment information
    assigned_to: Optional[UUID] = Field(
        None,
        description="Assignee user ID",
    )
    assigned_to_name: Optional[str] = Field(
        None,
        description="Assignee name",
    )
    assigned_to_role: Optional[str] = Field(
        None,
        description="Assignee role",
    )
    assigned_by: Optional[UUID] = Field(
        None,
        description="Assignor user ID",
    )
    assigned_by_name: Optional[str] = Field(
        None,
        description="Assignor name",
    )
    assigned_at: Optional[datetime] = Field(
        None,
        description="Assignment timestamp",
    )
    
    # Vendor information (if applicable)
    vendor_name: Optional[str] = Field(
        None,
        description="Vendor company name",
    )
    vendor_contact: Optional[str] = Field(
        None,
        description="Vendor contact number",
    )
    vendor_email: Optional[str] = Field(
        None,
        description="Vendor email",
    )
    
    # Status workflow
    status: MaintenanceStatus = Field(
        ...,
        description="Current status",
    )
    status_history: Optional[List[dict]] = Field(
        None,
        description="Status change history",
    )
    
    # Approval workflow
    requires_approval: bool = Field(
        default=False,
        description="Whether approval is required",
    )
    approval_pending: bool = Field(
        default=False,
        description="Whether approval is pending",
    )
    approved_by: Optional[UUID] = Field(
        None,
        description="Approver user ID",
    )
    approved_by_name: Optional[str] = Field(
        None,
        description="Approver name",
    )
    approved_at: Optional[datetime] = Field(
        None,
        description="Approval timestamp",
    )
    rejected_by: Optional[UUID] = Field(
        None,
        description="Rejector user ID",
    )
    rejected_at: Optional[datetime] = Field(
        None,
        description="Rejection timestamp",
    )
    rejection_reason: Optional[str] = Field(
        None,
        description="Rejection reason",
    )
    
    # Timeline
    started_at: Optional[datetime] = Field(
        None,
        description="Work start timestamp",
    )
    completed_at: Optional[datetime] = Field(
        None,
        description="Completion timestamp",
    )
    
    # Cost tracking
    estimated_cost: Optional[Decimal] = Field(
        None,
        description="Estimated cost",
    )
    actual_cost: Optional[Decimal] = Field(
        None,
        description="Actual cost incurred",
    )
    cost_approved: bool = Field(
        default=False,
        description="Whether cost was approved",
    )
    approval_threshold_exceeded: bool = Field(
        default=False,
        description="Whether cost exceeded approval threshold",
    )
    
    # Timeline estimates
    estimated_completion_date: Optional[date] = Field(
        None,
        description="Estimated completion date",
    )
    actual_completion_date: Optional[date] = Field(
        None,
        description="Actual completion date",
    )
    deadline: Optional[date] = Field(
        None,
        description="Completion deadline",
    )
    
    # Work details
    work_notes: Optional[str] = Field(
        None,
        description="Work performed notes",
    )
    materials_used: List[dict] = Field(
        default_factory=list,
        description="Materials used in work",
    )
    labor_hours: Optional[Decimal] = Field(
        None,
        description="Labor hours spent",
    )
    
    # Quality check
    quality_checked: bool = Field(
        default=False,
        description="Whether quality check was performed",
    )
    quality_checked_by: Optional[UUID] = Field(
        None,
        description="Quality checker user ID",
    )
    quality_check_passed: Optional[bool] = Field(
        None,
        description="Quality check result",
    )
    quality_check_notes: Optional[str] = Field(
        None,
        description="Quality check notes",
    )
    quality_checked_at: Optional[datetime] = Field(
        None,
        description="Quality check timestamp",
    )
    quality_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Quality rating (1-5 stars)",
    )
    
    # Preventive maintenance
    is_preventive: bool = Field(
        default=False,
        description="Whether this is preventive maintenance",
    )
    preventive_schedule_id: Optional[UUID] = Field(
        None,
        description="Related preventive schedule ID",
    )
    next_scheduled_date: Optional[date] = Field(
        None,
        description="Next scheduled maintenance date",
    )
    recurrence: Optional[str] = Field(
        None,
        description="Recurrence pattern",
    )
    
    # Warranty
    warranty_applicable: bool = Field(
        default=False,
        description="Whether warranty applies",
    )
    warranty_period_months: Optional[int] = Field(
        None,
        description="Warranty period in months",
    )
    warranty_expiry_date: Optional[date] = Field(
        None,
        description="Warranty expiry date",
    )

    @computed_field
    @property
    def is_completed(self) -> bool:
        """Check if maintenance is completed."""
        return self.status == MaintenanceStatus.COMPLETED

    @computed_field
    @property
    def is_active(self) -> bool:
        """Check if maintenance is currently active/in-progress."""
        active_statuses = {
            MaintenanceStatus.ASSIGNED,
            MaintenanceStatus.IN_PROGRESS,
        }
        return self.status in active_statuses

    @computed_field
    @property
    def cost_variance(self) -> Optional[Decimal]:
        """Calculate cost variance if both costs available."""
        if self.estimated_cost and self.actual_cost:
            return round(self.actual_cost - self.estimated_cost, 2)
        return None

    @computed_field
    @property
    def cost_variance_percentage(self) -> Optional[Decimal]:
        """Calculate cost variance percentage."""
        if self.estimated_cost and self.actual_cost and self.estimated_cost > 0:
            variance_pct = (
                (self.actual_cost - self.estimated_cost) / self.estimated_cost * 100
            )
            return round(variance_pct, 2)
        return None

    @computed_field
    @property
    def time_to_complete_days(self) -> Optional[int]:
        """Calculate total days from creation to completion."""
        if self.completed_at:
            return (self.completed_at - self.created_at).days
        return None


class RequestListItem(BaseSchema):
    """
    Minimal maintenance list item for efficient list rendering.
    
    Optimized for pagination and list views with minimal data transfer.
    """

    id: UUID = Field(
        ...,
        description="Maintenance request unique identifier",
    )
    request_number: str = Field(
        ...,
        description="Request number",
    )
    title: str = Field(
        ...,
        description="Issue title",
    )
    category: MaintenanceCategory = Field(
        ...,
        description="Category",
    )
    priority: Priority = Field(
        ...,
        description="Priority",
    )
    status: MaintenanceStatus = Field(
        ...,
        description="Status",
    )
    room_number: Optional[str] = Field(
        None,
        description="Room number",
    )
    estimated_cost: Optional[Decimal] = Field(
        None,
        description="Estimated cost",
    )
    assigned_to_name: Optional[str] = Field(
        None,
        description="Assignee name",
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp",
    )
    estimated_completion_date: Optional[date] = Field(
        None,
        description="Estimated completion",
    )

    @computed_field
    @property
    def status_badge_color(self) -> str:
        """Get color code for status badge (for UI rendering)."""
        color_map = {
            MaintenanceStatus.PENDING: "yellow",
            MaintenanceStatus.APPROVED: "blue",
            MaintenanceStatus.ASSIGNED: "cyan",
            MaintenanceStatus.IN_PROGRESS: "orange",
            MaintenanceStatus.ON_HOLD: "gray",
            MaintenanceStatus.COMPLETED: "green",
            MaintenanceStatus.REJECTED: "red",
            MaintenanceStatus.CANCELLED: "gray",
        }
        return color_map.get(self.status, "gray")

    @computed_field
    @property
    def priority_badge_color(self) -> str:
        """Get color code for priority badge."""
        color_map = {
            Priority.LOW: "green",
            Priority.MEDIUM: "yellow",
            Priority.HIGH: "orange",
            Priority.URGENT: "red",
            Priority.CRITICAL: "purple",
        }
        return color_map.get(self.priority, "gray")

    @computed_field
    @property
    def is_urgent(self) -> bool:
        """Check if request is urgent or critical."""
        return self.priority in [Priority.URGENT, Priority.CRITICAL]


class MaintenanceSummary(BaseSchema):
    """
    Maintenance summary statistics for hostel dashboard.
    
    Provides aggregated metrics for monitoring and reporting.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )
    period_start: Optional[date] = Field(
        None,
        description="Summary period start",
    )
    period_end: Optional[date] = Field(
        None,
        description="Summary period end",
    )
    
    # Request counts by status
    total_requests: int = Field(
        ...,
        ge=0,
        description="Total maintenance requests",
    )
    pending_requests: int = Field(
        ...,
        ge=0,
        description="Pending requests",
    )
    in_progress_requests: int = Field(
        ...,
        ge=0,
        description="In-progress requests",
    )
    completed_requests: int = Field(
        ...,
        ge=0,
        description="Completed requests",
    )
    on_hold_requests: int = Field(
        default=0,
        ge=0,
        description="On-hold requests",
    )
    cancelled_requests: int = Field(
        default=0,
        ge=0,
        description="Cancelled requests",
    )
    
    # Priority breakdown
    high_priority_count: int = Field(
        ...,
        ge=0,
        description="High priority requests",
    )
    urgent_priority_count: int = Field(
        ...,
        ge=0,
        description="Urgent priority requests",
    )
    critical_priority_count: int = Field(
        default=0,
        ge=0,
        description="Critical priority requests",
    )
    
    # Cost summary
    total_estimated_cost: Decimal = Field(
        ...,
        ge=0,
        description="Total estimated costs",
    )
    total_actual_cost: Decimal = Field(
        ...,
        ge=0,
        description="Total actual costs",
    )
    average_cost_per_request: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        description="Average cost per request",
    )
    
    # Performance metrics
    average_completion_time_hours: Decimal = Field(
        ...,
        ge=0,
        description="Average completion time in hours",
    )
    average_completion_time_days: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Average completion time in days",
    )
    on_time_completion_rate: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        le=100,
        description="Percentage completed on time",
    )
    
    # Quality metrics
    quality_check_pass_rate: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        le=100,
        description="Quality check pass rate",
    )
    average_quality_rating: Optional[Decimal] = Field(
        None,
        ge=0,
        le=5,
        description="Average quality rating",
    )
    
    # Category breakdown
    requests_by_category: Optional[dict] = Field(
        None,
        description="Request count by category",
    )

    @computed_field
    @property
    def completion_rate(self) -> Decimal:
        """Calculate completion rate percentage."""
        if self.total_requests == 0:
            return Decimal("0.00")
        return round(
            Decimal(self.completed_requests) / Decimal(self.total_requests) * 100,
            2,
        )

    @computed_field
    @property
    def cost_variance_total(self) -> Decimal:
        """Calculate total cost variance."""
        return round(self.total_actual_cost - self.total_estimated_cost, 2)