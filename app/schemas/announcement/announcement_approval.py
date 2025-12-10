"""
Announcement approval schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class ApprovalRequest(BaseCreateSchema):
    """Request approval for announcement (supervisor to admin)"""
    announcement_id: UUID
    
    # Justification
    approval_reason: Optional[str] = Field(None, max_length=500, description="Why approval needed")
    
    # Urgency
    is_urgent_request: bool = Field(False)


class ApprovalResponse(BaseSchema):
    """Approval response"""
    announcement_id: UUID
    
    approved: bool
    approved_by: UUID
    approved_by_name: str
    approved_at: datetime
    
    # Feedback
    approval_notes: Optional[str]
    
    # If approved, auto-publish?
    auto_published: bool
    
    message: str


class RejectionRequest(BaseCreateSchema):
    """Reject announcement"""
    announcement_id: UUID
    
    rejection_reason: str = Field(..., min_length=20, max_length=500)
    
    # Suggestions
    suggested_modifications: Optional[str] = Field(None, max_length=1000)


class ApprovalWorkflow(BaseSchema):
    """Approval workflow status"""
    announcement_id: UUID
    title: str
    
    requires_approval: bool
    approval_status: str = Field(
        ...,
        pattern="^(pending|approved|rejected|not_required)$"
    )
    
    # Submitted by
    created_by: UUID
    created_by_name: str
    created_by_role: str
    
    # Approval timeline
    submitted_for_approval_at: Optional[datetime]
    approved_rejected_at: Optional[datetime]
    
    # Current approver
    pending_with: Optional[UUID]
    pending_with_name: Optional[str]
    
    # Reason (if rejected)
    rejection_reason: Optional[str]


class SupervisorApprovalQueue(BaseSchema):
    """Supervisor's pending approvals"""
    supervisor_id: UUID
    supervisor_name: str
    
    total_pending: int
    urgent_pending: int
    
    pending_announcements: List["PendingApprovalItem"]


class PendingApprovalItem(BaseSchema):
    """Pending approval item"""
    announcement_id: UUID
    title: str
    category: str
    
    created_by: UUID
    created_by_name: str
    
    submitted_at: datetime
    is_urgent: bool
    
    # Preview
    content_preview: str = Field(..., description="First 200 chars")
    
    target_audience: str
    estimated_recipients: int


class BulkApproval(BaseCreateSchema):
    """Approve multiple announcements"""
    announcement_ids: List[UUID] = Field(..., min_items=1)
    
    approved: bool
    approval_notes: Optional[str] = None
    
    # Publish immediately after approval
    publish_immediately: bool = Field(True)