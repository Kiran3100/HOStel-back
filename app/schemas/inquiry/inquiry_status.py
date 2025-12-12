# --- File: app/schemas/inquiry/inquiry_status.py ---
"""
<<<<<<< Updated upstream
Inquiry status management schemas.

This module defines schemas for managing inquiry status changes,
assignments, timeline tracking, and follow-ups.
=======
Inquiry status management, assignment, and timeline schemas.

This module handles all status transitions, assignments, and
maintains an audit trail of inquiry lifecycle events.
>>>>>>> Stashed changes
"""

from __future__ import annotations

from datetime import datetime
<<<<<<< Updated upstream
from typing import List, Optional
=======
from typing import Optional
>>>>>>> Stashed changes
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.common.enums import InquiryStatus

__all__ = [
    "InquiryStatusUpdate",
    "InquiryAssignment",
<<<<<<< Updated upstream
    "InquiryFollowUp",
    "InquiryTimelineEntry",
    "InquiryConversion",
    "BulkInquiryStatusUpdate",
]


class InquiryStatusUpdate(BaseCreateSchema):
    """
    Update inquiry status with notes.
    
    Used to track status changes throughout the inquiry lifecycle.
    """

    inquiry_id: UUID = Field(
        ...,
        description="Inquiry ID to update",
    )
    new_status: InquiryStatus = Field(
        ...,
        description="New status to set",
    )
    notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Notes about status change",
    )

    # Metadata
    updated_by: Optional[UUID] = Field(
        None,
        description="Admin updating the status",
    )

    @field_validator("notes")
    @classmethod
    def clean_notes(cls, v: Optional[str]) -> Optional[str]:
        """Clean notes field."""
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
        return v

    @model_validator(mode="after")
    def validate_status_transition(self) -> "InquiryStatusUpdate":
        """
        Validate status transition is logical.
        
        Note: This is a soft validation - enforces best practices
        but doesn't block unusual transitions (admin override).
        """
        # Define logical status transitions
        valid_transitions = {
            InquiryStatus.NEW: [
                InquiryStatus.CONTACTED,
                InquiryStatus.NOT_INTERESTED,
            ],
            InquiryStatus.CONTACTED: [
                InquiryStatus.INTERESTED,
                InquiryStatus.NOT_INTERESTED,
                InquiryStatus.CONVERTED,
            ],
            InquiryStatus.INTERESTED: [
                InquiryStatus.CONVERTED,
                InquiryStatus.NOT_INTERESTED,
            ],
            InquiryStatus.NOT_INTERESTED: [],  # Terminal state
            InquiryStatus.CONVERTED: [],  # Terminal state
        }
        
        # This validation would need access to current status
        # In practice, this would be validated at the service layer
        # where we have access to the current inquiry data
=======
    "InquiryTimelineEntry",
    "InquiryStatusTransition",
    "BulkInquiryStatusUpdate",
    "InquiryEscalation",
]

# Valid status transitions mapping
VALID_STATUS_TRANSITIONS: dict[InquiryStatus, set[InquiryStatus]] = {
    InquiryStatus.NEW: {
        InquiryStatus.CONTACTED,
        InquiryStatus.NOT_INTERESTED,
    },
    InquiryStatus.CONTACTED: {
        InquiryStatus.INTERESTED,
        InquiryStatus.NOT_INTERESTED,
        InquiryStatus.CONVERTED,
    },
    InquiryStatus.INTERESTED: {
        InquiryStatus.CONTACTED,  # Re-contact
        InquiryStatus.NOT_INTERESTED,
        InquiryStatus.CONVERTED,
    },
    InquiryStatus.NOT_INTERESTED: {
        InquiryStatus.CONTACTED,  # Re-engagement
        InquiryStatus.INTERESTED,
    },
    InquiryStatus.CONVERTED: set(),  # Terminal state
}


class InquiryStatusTransition(BaseSchema):
    """
    Defines valid status transitions for inquiries.
    
    Used for validation and UI state management.
    """
    
    from_status: InquiryStatus = Field(
        ...,
        description="Current status",
    )
    to_status: InquiryStatus = Field(
        ...,
        description="Target status",
    )
    is_valid: bool = Field(
        ...,
        description="Whether transition is valid",
    )
    requires_reason: bool = Field(
        False,
        description="Whether reason is required for this transition",
    )
    
    @classmethod
    def check_transition(
        cls,
        from_status: InquiryStatus,
        to_status: InquiryStatus,
    ) -> "InquiryStatusTransition":
        """Check if a status transition is valid."""
        valid_targets = VALID_STATUS_TRANSITIONS.get(from_status, set())
        is_valid = to_status in valid_targets
        
        # Require reason for certain transitions
        requires_reason = to_status == InquiryStatus.NOT_INTERESTED
        
        return cls(
            from_status=from_status,
            to_status=to_status,
            is_valid=is_valid,
            requires_reason=requires_reason,
        )
    
    @classmethod
    def get_valid_transitions(
        cls,
        current_status: InquiryStatus,
    ) -> list[InquiryStatus]:
        """Get list of valid target statuses from current status."""
        return list(VALID_STATUS_TRANSITIONS.get(current_status, set()))


class InquiryStatusUpdate(BaseCreateSchema):
    """
    Schema for updating inquiry status with audit trail.
    
    Validates status transitions and captures reason/notes
    for the change.
    """
    
    inquiry_id: UUID = Field(
        ...,
        description="UUID of the inquiry to update",
    )
    current_status: InquiryStatus = Field(
        ...,
        description="Current status (for validation)",
    )
    new_status: InquiryStatus = Field(
        ...,
        description="Target status",
    )
    reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Reason for status change",
    )
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional notes about the change",
    )
    updated_by: UUID = Field(
        ...,
        description="UUID of user making the change",
    )
    
    @model_validator(mode="after")
    def validate_status_transition(self) -> "InquiryStatusUpdate":
        """Validate that the status transition is allowed."""
        if self.current_status == self.new_status:
            raise ValueError("New status must be different from current status")
        
        transition = InquiryStatusTransition.check_transition(
            self.current_status,
            self.new_status,
        )
        
        if not transition.is_valid:
            valid_statuses = InquiryStatusTransition.get_valid_transitions(
                self.current_status
            )
            valid_str = ", ".join(s.value for s in valid_statuses)
            raise ValueError(
                f"Invalid status transition from '{self.current_status.value}' "
                f"to '{self.new_status.value}'. "
                f"Valid transitions: {valid_str or 'none (terminal state)'}"
            )
        
        if transition.requires_reason and not self.reason:
            raise ValueError(
                f"Reason is required when changing status to "
                f"'{self.new_status.value}'"
            )
>>>>>>> Stashed changes
        
        return self


class InquiryAssignment(BaseCreateSchema):
    """
<<<<<<< Updated upstream
    Assign inquiry to an admin/staff member.
    
    Used for distributing inquiries among team members
    for follow-up.
    """

    inquiry_id: UUID = Field(
        ...,
        description="Inquiry ID to assign",
    )
    assigned_to: UUID = Field(
        ...,
        description="Admin/staff member to assign to",
    )
    assigned_by: UUID = Field(
        ...,
        description="Admin making the assignment",
    )

=======
    Schema for assigning an inquiry to staff member.
    
    Tracks assignment with full audit information.
    """
    
    inquiry_id: UUID = Field(
        ...,
        description="UUID of the inquiry to assign",
    )
    assigned_to: UUID = Field(
        ...,
        description="UUID of the user being assigned",
    )
    assigned_by: UUID = Field(
        ...,
        description="UUID of the user making the assignment",
    )
>>>>>>> Stashed changes
    assignment_notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Notes about the assignment",
    )
<<<<<<< Updated upstream

    # Due Date for Follow-up
    follow_up_due: Optional[datetime] = Field(
        None,
        description="When follow-up should be completed by",
    )

    @field_validator("assignment_notes")
    @classmethod
    def clean_notes(cls, v: Optional[str]) -> Optional[str]:
        """Clean assignment notes."""
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
        return v

    @field_validator("follow_up_due")
    @classmethod
    def validate_follow_up_due(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate follow-up due date."""
        if v is not None:
            if v < datetime.utcnow():
                raise ValueError("Follow-up due date cannot be in the past")
        return v


class InquiryFollowUp(BaseCreateSchema):
    """
    Record a follow-up action on an inquiry.
    
    Used to track all interactions with the visitor.
    """

    inquiry_id: UUID = Field(
        ...,
        description="Inquiry ID",
    )
    followed_up_by: UUID = Field(
        ...,
        description="Admin who performed follow-up",
    )

    # Follow-up Details
    contact_method: str = Field(
        ...,
        pattern=r"^(phone|email|sms|whatsapp|in_person|other)$",
        description="Method of contact",
    )
    contact_outcome: str = Field(
        ...,
        pattern=r"^(connected|no_answer|voicemail|email_sent|interested|not_interested|callback_requested)$",
        description="Outcome of the follow-up attempt",
    )

    # Notes
    notes: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Detailed notes about the follow-up",
    )

    # Next Steps
    next_follow_up_date: Optional[datetime] = Field(
        None,
        description="When next follow-up should occur",
    )

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, v: str) -> str:
        """Validate notes are meaningful."""
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Follow-up notes must be at least 10 characters")
        return v

    @field_validator("next_follow_up_date")
    @classmethod
    def validate_next_follow_up(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate next follow-up date."""
        if v is not None:
            if v < datetime.utcnow():
                raise ValueError("Next follow-up date cannot be in the past")
=======
    priority: str = Field(
        "normal",
        pattern=r"^(low|normal|high|urgent)$",
        description="Assignment priority level",
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Due date for follow-up",
    )
    
    @field_validator("assigned_to")
    @classmethod
    def validate_not_self_assign(cls, v: UUID, info) -> UUID:
        """Prevent self-assignment (optional business rule)."""
        # Note: This validation may need to be adjusted based on
        # business requirements. Some systems allow self-assignment.
        assigned_by = info.data.get("assigned_by")
        if v == assigned_by:
            # Currently allowing self-assignment with a note
            pass
        return v
    
    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Ensure due date is in the future."""
        if v and v < datetime.utcnow():
            raise ValueError("Due date must be in the future")
>>>>>>> Stashed changes
        return v


class InquiryTimelineEntry(BaseSchema):
    """
<<<<<<< Updated upstream
    Timeline entry for inquiry lifecycle.
    
    Represents a single event in the inquiry's history.
    """

    event_type: str = Field(
        ...,
        pattern=r"^(status_change|assignment|follow_up|note_added|conversion)$",
        description="Type of timeline event",
    )
    status: Optional[InquiryStatus] = Field(
        None,
        description="Status at this point (for status_change events)",
    )
    timestamp: datetime = Field(
        ...,
        description="When this event occurred",
    )
    changed_by: Optional[UUID] = Field(
        None,
        description="Admin who triggered this event",
    )
    changed_by_name: Optional[str] = Field(
        None,
        description="Name of admin who triggered event",
=======
    Timeline record for tracking inquiry lifecycle events.
    
    Creates an immutable audit trail of all actions taken
    on an inquiry.
    """
    
    id: UUID = Field(
        ...,
        description="Timeline entry UUID",
    )
    inquiry_id: UUID = Field(
        ...,
        description="Associated inquiry UUID",
    )
    
    # Event type
    event_type: str = Field(
        ...,
        pattern=r"^(status_change|assignment|contact|note|escalation|conversion)$",
        description="Type of timeline event",
    )
    
    # Status tracking (for status_change events)
    previous_status: Optional[InquiryStatus] = Field(
        None,
        description="Previous status (for status changes)",
    )
    new_status: Optional[InquiryStatus] = Field(
        None,
        description="New status (for status changes)",
    )
    
    # Event details
    description: str = Field(
        ...,
        max_length=500,
        description="Human-readable description of the event",
>>>>>>> Stashed changes
    )
    notes: Optional[str] = Field(
        None,
        max_length=1000,
<<<<<<< Updated upstream
        description="Notes about this event",
    )

    # Additional Context
    metadata: dict = Field(
        default_factory=dict,
        description="Additional event metadata",
    )


class InquiryConversion(BaseCreateSchema):
    """
    Record inquiry conversion to booking.
    
    Links inquiry to the resulting booking.
    """

    inquiry_id: UUID = Field(
        ...,
        description="Inquiry ID that converted",
    )
    booking_id: UUID = Field(
        ...,
        description="Resulting booking ID",
    )
    converted_by: UUID = Field(
        ...,
        description="Admin who facilitated conversion",
    )

    conversion_notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Notes about the conversion",
    )

    @field_validator("conversion_notes")
    @classmethod
    def clean_notes(cls, v: Optional[str]) -> Optional[str]:
        """Clean conversion notes."""
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
        return v
=======
        description="Additional notes",
    )
    
    # Audit information
    performed_by: UUID = Field(
        ...,
        description="UUID of user who performed the action",
    )
    performed_by_name: str = Field(
        ...,
        description="Name of user who performed the action",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the event occurred",
    )
    
    # Additional context
    metadata: Optional[dict] = Field(
        None,
        description="Additional event metadata",
    )
    
    @classmethod
    def create_status_change_entry(
        cls,
        inquiry_id: UUID,
        previous_status: InquiryStatus,
        new_status: InquiryStatus,
        performed_by: UUID,
        performed_by_name: str,
        notes: Optional[str] = None,
    ) -> dict:
        """
        Factory method for creating status change timeline entries.
        
        Returns dict for database insertion.
        """
        return {
            "inquiry_id": inquiry_id,
            "event_type": "status_change",
            "previous_status": previous_status,
            "new_status": new_status,
            "description": (
                f"Status changed from '{previous_status.value}' "
                f"to '{new_status.value}'"
            ),
            "notes": notes,
            "performed_by": performed_by,
            "performed_by_name": performed_by_name,
            "timestamp": datetime.utcnow(),
        }
    
    @classmethod
    def create_assignment_entry(
        cls,
        inquiry_id: UUID,
        assigned_to_name: str,
        performed_by: UUID,
        performed_by_name: str,
        notes: Optional[str] = None,
    ) -> dict:
        """Factory method for creating assignment timeline entries."""
        return {
            "inquiry_id": inquiry_id,
            "event_type": "assignment",
            "description": f"Assigned to {assigned_to_name}",
            "notes": notes,
            "performed_by": performed_by,
            "performed_by_name": performed_by_name,
            "timestamp": datetime.utcnow(),
        }
>>>>>>> Stashed changes


class BulkInquiryStatusUpdate(BaseCreateSchema):
    """
<<<<<<< Updated upstream
    Update status of multiple inquiries.
    
    Used for batch operations on inquiries.
    """

    inquiry_ids: List[UUID] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of inquiry IDs to update (max 100)",
    )
    new_status: InquiryStatus = Field(
        ...,
        description="New status for all inquiries",
    )
    notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Common notes for all updates",
    )

    updated_by: UUID = Field(
        ...,
        description="Admin performing bulk update",
    )

    @field_validator("inquiry_ids")
    @classmethod
    def validate_inquiry_ids(cls, v: List[UUID]) -> List[UUID]:
        """Validate inquiry IDs list."""
        if len(v) == 0:
            raise ValueError("At least one inquiry ID is required")
        
        if len(v) > 100:
            raise ValueError("Maximum 100 inquiries can be updated at once")
        
        # Remove duplicates
        unique_ids = list(dict.fromkeys(v))
        
        return unique_ids

    @field_validator("notes")
    @classmethod
    def clean_notes(cls, v: Optional[str]) -> Optional[str]:
        """Clean notes."""
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
=======
    Schema for bulk status updates on multiple inquiries.
    
    Used for batch operations in admin interfaces.
    """
    
    inquiry_ids: list[UUID] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of inquiry UUIDs to update (max 100)",
    )
    new_status: InquiryStatus = Field(
        ...,
        description="Target status for all inquiries",
    )
    reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Reason for bulk status change",
    )
    updated_by: UUID = Field(
        ...,
        description="UUID of user making the changes",
    )
    skip_invalid: bool = Field(
        True,
        description="Skip inquiries with invalid transitions instead of failing",
    )
    
    @field_validator("inquiry_ids")
    @classmethod
    def validate_unique_ids(cls, v: list[UUID]) -> list[UUID]:
        """Ensure all inquiry IDs are unique."""
        if len(v) != len(set(v)):
            raise ValueError("Duplicate inquiry IDs are not allowed")
        return v


class InquiryEscalation(BaseCreateSchema):
    """
    Schema for escalating an inquiry to higher authority.
    
    Used when an inquiry requires attention from senior staff
    or management.
    """
    
    inquiry_id: UUID = Field(
        ...,
        description="UUID of the inquiry to escalate",
    )
    escalated_to: UUID = Field(
        ...,
        description="UUID of the user to escalate to",
    )
    escalated_by: UUID = Field(
        ...,
        description="UUID of the user escalating",
    )
    escalation_reason: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Reason for escalation",
    )
    priority: str = Field(
        "high",
        pattern=r"^(high|urgent|critical)$",
        description="Escalation priority level",
    )
    response_required_by: Optional[datetime] = Field(
        None,
        description="Deadline for response",
    )
    
    @field_validator("escalated_to")
    @classmethod
    def validate_different_users(cls, v: UUID, info) -> UUID:
        """Ensure escalation is to a different user."""
        escalated_by = info.data.get("escalated_by")
        if v == escalated_by:
            raise ValueError("Cannot escalate to yourself")
        return v
    
    @field_validator("response_required_by")
    @classmethod
    def validate_deadline(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Ensure deadline is in the future."""
        if v and v < datetime.utcnow():
            raise ValueError("Response deadline must be in the future")
>>>>>>> Stashed changes
        return v