"""
Menu approval schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class MenuApprovalRequest(BaseCreateSchema):
    """Request menu approval (supervisor to admin)"""
    menu_id: UUID
    
    # Submission notes
    submission_notes: Optional[str] = Field(None, max_length=500)
    
    # Budget info
    estimated_cost_per_person: Optional[Decimal] = None


class MenuApprovalResponse(BaseSchema):
    """Menu approval response"""
    menu_id: UUID
    menu_date: date
    
    approved: bool
    approved_by: UUID
    approved_by_name: str
    approved_at: datetime
    
    # Feedback
    approval_notes: Optional[str]
    
    message: str


class ApprovalWorkflow(BaseSchema):
    """Menu approval workflow status"""
    menu_id: UUID
    menu_date: date
    
    requires_approval: bool
    approval_status: str = Field(
        ...,
        pattern="^(pending|approved|rejected|not_required)$"
    )
    
    # Timeline
    submitted_for_approval_at: Optional[datetime]
    approved_at: Optional[datetime]
    rejected_at: Optional[datetime]
    
    # Approver
    pending_with: Optional[UUID]
    pending_with_name: Optional[str]


class BulkApproval(BaseCreateSchema):
    """Approve multiple menus"""
    menu_ids: List[UUID] = Field(..., min_items=1)
    
    approved: bool
    approval_notes: Optional[str] = None