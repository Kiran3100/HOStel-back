"""
Complaint assignment schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class AssignmentRequest(BaseCreateSchema):
    """Assign complaint to staff member"""
    complaint_id: UUID = Field(..., description="Complaint ID")
    assigned_to: UUID = Field(..., description="User ID to assign to (supervisor/staff)")
    
    # Optional
    estimated_resolution_time: Optional[datetime] = Field(
        None,
        description="Estimated resolution time"
    )
    
    assignment_notes: Optional[str] = Field(None, max_length=500)


class AssignmentResponse(BaseSchema):
    """Assignment response"""
    complaint_id: UUID
    complaint_number: str
    
    assigned_to: UUID
    assigned_to_name: str
    assigned_by: UUID
    assigned_by_name: str
    
    assigned_at: datetime
    
    message: str


class ReassignmentRequest(BaseCreateSchema):
    """Reassign complaint to different staff"""
    complaint_id: UUID
    new_assigned_to: UUID = Field(..., description="New assignee")
    
    reassignment_reason: str = Field(..., min_length=10, max_length=500)
    
    # Notify previous assignee
    notify_previous_assignee: bool = Field(True)


class BulkAssignment(BaseCreateSchema):
    """Assign multiple complaints"""
    complaint_ids: List[UUID] = Field(..., min_items=1)
    assigned_to: UUID
    
    assignment_notes: Optional[str] = None


class UnassignRequest(BaseCreateSchema):
    """Unassign complaint"""
    complaint_id: UUID
    reason: str = Field(..., min_length=10, max_length=500)