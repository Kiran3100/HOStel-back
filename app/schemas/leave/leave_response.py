# --- File: app/schemas/leave/leave_response.py ---
"""
Leave response schemas for API responses.

Provides various response formats for leave data including
detailed, summary, and list views with computed fields.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import Field, computed_field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import LeaveStatus, LeaveType

__all__ = [
    "LeaveResponse",
    "LeaveDetail",
    "LeaveListItem",
    "LeaveSummary",
]


class LeaveResponse(BaseResponseSchema):
    """
    Standard leave response with essential information.
    
    Lightweight response schema for list views and basic queries.
    """

    student_id: UUID = Field(
        ...,
        description="Student unique identifier",
    )
    student_name: str = Field(
        ...,
        description="Student full name",
    )
    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )
    leave_type: LeaveType = Field(
        ...,
        description="Type of leave",
    )
    from_date: date = Field(
        ...,
        description="Leave start date",
    )
    to_date: date = Field(
        ...,
        description="Leave end date",
    )
    total_days: int = Field(
        ...,
        description="Total leave days",
    )
    status: LeaveStatus = Field(
        ...,
        description="Current leave status",
    )
    applied_at: datetime = Field(
        ...,
        description="Application submission timestamp",
    )
    reason: Optional[str] = Field(
        None,
        description="Leave reason (truncated for list view)",
    )

    @computed_field
    @property
    def status_display(self) -> str:
        """Human-readable status display."""
        status_map = {
            LeaveStatus.PENDING: "Pending Approval",
            LeaveStatus.APPROVED: "Approved",
            LeaveStatus.REJECTED: "Rejected",
            LeaveStatus.CANCELLED: "Cancelled",
        }
        return status_map.get(self.status, self.status.value)

    @computed_field
    @property
    def leave_type_display(self) -> str:
        """Human-readable leave type display."""
        type_map = {
            LeaveType.CASUAL: "Casual Leave",
            LeaveType.SICK: "Sick Leave",
            LeaveType.EMERGENCY: "Emergency Leave",
            LeaveType.VACATION: "Vacation",
            LeaveType.OTHER: "Other",
        }
        return type_map.get(self.leave_type, self.leave_type.value)

    @computed_field
    @property
    def is_active(self) -> bool:
        """Check if leave is currently active."""
        if self.status != LeaveStatus.APPROVED:
            return False
        
        today = date.today()
        return self.from_date <= today <= self.to_date

    @computed_field
    @property
    def days_remaining(self) -> Optional[int]:
        """Calculate remaining days for active leave."""
        if not self.is_active:
            return None
        
        return (self.to_date - date.today()).days + 1


class LeaveDetail(BaseResponseSchema):
    """
    Detailed leave information with complete metadata.
    
    Comprehensive response including all leave details, approval workflow,
    and supporting information.
    """

    student_id: UUID = Field(
        ...,
        description="Student unique identifier",
    )
    student_name: str = Field(
        ...,
        description="Student full name",
    )
    student_email: Optional[str] = Field(
        None,
        description="Student email address",
    )
    student_phone: Optional[str] = Field(
        None,
        description="Student phone number",
    )
    student_room: Optional[str] = Field(
        None,
        description="Student room number",
    )
    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )

    # Leave details
    leave_type: LeaveType = Field(
        ...,
        description="Type of leave",
    )
    from_date: date = Field(
        ...,
        description="Leave start date",
    )
    to_date: date = Field(
        ...,
        description="Leave end date",
    )
    total_days: int = Field(
        ...,
        description="Total leave days",
    )
    reason: str = Field(
        ...,
        description="Detailed leave reason",
    )

    # Contact information
    contact_during_leave: Optional[str] = Field(
        None,
        description="Contact number during leave",
    )
    emergency_contact: Optional[str] = Field(
        None,
        description="Emergency contact number",
    )
    emergency_contact_relation: Optional[str] = Field(
        None,
        description="Relation with emergency contact",
    )
    destination_address: Optional[str] = Field(
        None,
        description="Destination address",
    )

    # Supporting documents
    supporting_document_url: Optional[str] = Field(
        None,
        description="Supporting document URL",
    )

    # Status and workflow
    status: LeaveStatus = Field(
        ...,
        description="Current leave status",
    )
    applied_at: datetime = Field(
        ...,
        description="Application submission timestamp",
    )

    # Approval details
    approved_at: Optional[datetime] = Field(
        None,
        description="Approval timestamp",
    )
    approved_by: Optional[UUID] = Field(
        None,
        description="Approver user ID",
    )
    approved_by_name: Optional[str] = Field(
        None,
        description="Approver name",
    )
    approval_notes: Optional[str] = Field(
        None,
        description="Approval notes",
    )
    conditions: Optional[str] = Field(
        None,
        description="Approval conditions",
    )

    # Rejection details
    rejected_at: Optional[datetime] = Field(
        None,
        description="Rejection timestamp",
    )
    rejected_by: Optional[UUID] = Field(
        None,
        description="Rejector user ID",
    )
    rejected_by_name: Optional[str] = Field(
        None,
        description="Rejector name",
    )
    rejection_reason: Optional[str] = Field(
        None,
        description="Rejection reason",
    )

    # Cancellation details
    cancelled_at: Optional[datetime] = Field(
        None,
        description="Cancellation timestamp",
    )
    cancelled_by: Optional[UUID] = Field(
        None,
        description="User who cancelled",
    )
    cancellation_reason: Optional[str] = Field(
        None,
        description="Cancellation reason",
    )

    # Additional metadata
    last_modified_at: Optional[datetime] = Field(
        None,
        description="Last modification timestamp",
    )
    last_modified_by: Optional[UUID] = Field(
        None,
        description="Last modifier user ID",
    )

    @computed_field
    @property
    def is_active(self) -> bool:
        """Check if leave is currently active."""
        if self.status != LeaveStatus.APPROVED:
            return False
        
        today = date.today()
        return self.from_date <= today <= self.to_date

    @computed_field
    @property
    def is_upcoming(self) -> bool:
        """Check if leave is upcoming."""
        if self.status != LeaveStatus.APPROVED:
            return False
        
        return self.from_date > date.today()

    @computed_field
    @property
    def is_past(self) -> bool:
        """Check if leave is in the past."""
        return self.to_date < date.today()

    @computed_field
    @property
    def can_be_cancelled(self) -> bool:
        """Check if leave can be cancelled by student."""
        # Can only cancel pending or approved (future/ongoing) leaves
        if self.status not in [LeaveStatus.PENDING, LeaveStatus.APPROVED]:
            return False
        
        # Can't cancel past leaves
        if self.is_past:
            return False
        
        return True


class LeaveListItem(BaseSchema):
    """
    Minimal leave list item for efficient list rendering.
    
    Optimized for pagination and list views with minimal data transfer.
    """

    id: UUID = Field(
        ...,
        description="Leave application unique identifier",
    )
    student_id: UUID = Field(
        ...,
        description="Student unique identifier",
    )
    student_name: str = Field(
        ...,
        description="Student name",
    )
    room_number: Optional[str] = Field(
        None,
        description="Room number",
    )
    leave_type: LeaveType = Field(
        ...,
        description="Leave type",
    )
    from_date: date = Field(
        ...,
        description="Start date",
    )
    to_date: date = Field(
        ...,
        description="End date",
    )
    total_days: int = Field(
        ...,
        description="Total days",
    )
    status: LeaveStatus = Field(
        ...,
        description="Leave status",
    )
    applied_at: datetime = Field(
        ...,
        description="Application date",
    )

    @computed_field
    @property
    def status_badge_color(self) -> str:
        """Get color code for status badge (for UI rendering)."""
        color_map = {
            LeaveStatus.PENDING: "yellow",
            LeaveStatus.APPROVED: "green",
            LeaveStatus.REJECTED: "red",
            LeaveStatus.CANCELLED: "gray",
        }
        return color_map.get(self.status, "gray")

    @computed_field
    @property
    def is_urgent(self) -> bool:
        """Check if leave requires urgent attention."""
        # Pending leaves starting soon are urgent
        if self.status == LeaveStatus.PENDING:
            days_until_start = (self.from_date - date.today()).days
            return days_until_start <= 2
        return False


class LeaveSummary(BaseSchema):
    """
    Leave summary statistics for dashboard.
    
    Provides aggregated view of leave status for reporting.
    """

    student_id: Optional[UUID] = Field(
        None,
        description="Student ID (if student-specific summary)",
    )
    hostel_id: Optional[UUID] = Field(
        None,
        description="Hostel ID (if hostel-specific summary)",
    )
    period_start: date = Field(
        ...,
        description="Summary period start date",
    )
    period_end: date = Field(
        ...,
        description="Summary period end date",
    )

    # Count by status
    total_applications: int = Field(
        ...,
        ge=0,
        description="Total leave applications",
    )
    pending_count: int = Field(
        ...,
        ge=0,
        description="Pending applications",
    )
    approved_count: int = Field(
        ...,
        ge=0,
        description="Approved applications",
    )
    rejected_count: int = Field(
        ...,
        ge=0,
        description="Rejected applications",
    )
    cancelled_count: int = Field(
        ...,
        ge=0,
        description="Cancelled applications",
    )

    # Count by type
    casual_count: int = Field(
        default=0,
        ge=0,
        description="Casual leave count",
    )
    sick_count: int = Field(
        default=0,
        ge=0,
        description="Sick leave count",
    )
    emergency_count: int = Field(
        default=0,
        ge=0,
        description="Emergency leave count",
    )
    vacation_count: int = Field(
        default=0,
        ge=0,
        description="Vacation count",
    )

    # Day statistics
    total_days_requested: int = Field(
        ...,
        ge=0,
        description="Total days requested across all applications",
    )
    total_days_approved: int = Field(
        ...,
        ge=0,
        description="Total days approved",
    )
    active_leaves: int = Field(
        default=0,
        ge=0,
        description="Currently active leaves",
    )

    @computed_field
    @property
    def approval_rate(self) -> float:
        """Calculate approval rate percentage."""
        total_decided = self.approved_count + self.rejected_count
        if total_decided == 0:
            return 0.0
        return round((self.approved_count / total_decided) * 100, 2)