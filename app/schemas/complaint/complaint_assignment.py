"""
Complaint assignment schemas with enhanced validation and business logic.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class AssignmentRequest(BaseCreateSchema):
    """Assign complaint to staff member with validation."""
    
    complaint_id: UUID = Field(..., description="Complaint ID")
    assigned_to: UUID = Field(..., description="User ID to assign to (supervisor/staff)")
    
    # Optional
    estimated_resolution_time: Optional[datetime] = Field(
        None,
        description="Estimated resolution time"
    )
    
    assignment_notes: Optional[str] = Field(None, min_length=5, max_length=500)

    @field_validator("estimated_resolution_time")
    @classmethod
    def validate_future_time(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Ensure estimated time is in the future."""
        if v and v <= datetime.utcnow():
            raise ValueError("Estimated resolution time must be in the future")
        return v

    @field_validator("assignment_notes")
    @classmethod
    def validate_notes(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize assignment notes."""
        if v:
            v = v.strip()
            if len(v) < 5:
                raise ValueError("Assignment notes must be at least 5 characters")
        return v


class AssignmentResponse(BaseSchema):
    """Assignment response with complete information."""
    
    complaint_id: UUID
    complaint_number: str
    
    assigned_to: UUID
    assigned_to_name: str
    assigned_by: UUID
    assigned_by_name: str
    
    assigned_at: datetime
    
    message: str

    @classmethod
    def create(
        cls,
        complaint_id: UUID,
        complaint_number: str,
        assigned_to: UUID,
        assigned_to_name: str,
        assigned_by: UUID,
        assigned_by_name: str
    ) -> "AssignmentResponse":
        """Factory method to create assignment response."""
        return cls(
            complaint_id=complaint_id,
            complaint_number=complaint_number,
            assigned_to=assigned_to,
            assigned_to_name=assigned_to_name,
            assigned_by=assigned_by,
            assigned_by_name=assigned_by_name,
            assigned_at=datetime.utcnow(),
            message=f"Complaint {complaint_number} assigned to {assigned_to_name}"
        )


class ReassignmentRequest(BaseCreateSchema):
    """Reassign complaint to different staff with validation."""
    
    complaint_id: UUID
    new_assigned_to: UUID = Field(..., description="New assignee")
    
    reassignment_reason: str = Field(..., min_length=10, max_length=500)
    
    # Notify previous assignee
    notify_previous_assignee: bool = Field(True)

    @field_validator("reassignment_reason")
    @classmethod
    def validate_reason(cls, v: str) -> str:
        """Validate reassignment reason is meaningful."""
        v = v.strip()
        if len(v.split()) < 3:
            raise ValueError("Reassignment reason must contain at least 3 words")
        return v

    @model_validator(mode="after")
    def validate_not_self_assignment(self) -> "ReassignmentRequest":
        """Ensure not reassigning to same person (would need current assignee info)."""
        # This validation would be done at the service level with database access
        return self


class BulkAssignment(BaseCreateSchema):
    """Assign multiple complaints with validation."""
    
    complaint_ids: List[UUID] = Field(..., min_items=1, max_items=50)
    assigned_to: UUID
    
    assignment_notes: Optional[str] = Field(None, max_length=500)

    @field_validator("complaint_ids")
    @classmethod
    def validate_unique_ids(cls, v: List[UUID]) -> List[UUID]:
        """Ensure complaint IDs are unique."""
        if len(v) != len(set(v)):
            raise ValueError("Duplicate complaint IDs not allowed")
        return v


class UnassignRequest(BaseCreateSchema):
    """Unassign complaint with reason."""
    
    complaint_id: UUID
    reason: str = Field(..., min_length=10, max_length=500)

    @field_validator("reason")
    @classmethod
    def validate_unassign_reason(cls, v: str) -> str:
        """Validate unassignment reason."""
        v = v.strip()
        if len(v.split()) < 3:
            raise ValueError("Unassignment reason must contain at least 3 words")
        return v