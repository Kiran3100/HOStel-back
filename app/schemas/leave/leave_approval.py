"""
Leave approval & workflow schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.common.enums import LeaveStatus


class LeaveApprovalRequest(BaseCreateSchema):
    """Supervisor/admin leave approval/rejection"""
    leave_id: UUID
    approver_id: UUID

    approve: bool
    approval_notes: Optional[str] = Field(
        None, max_length=500, description="Additional notes"
    )

    # If rejecting
    rejection_reason: Optional[str] = Field(None, max_length=500)


class LeaveApprovalResponse(BaseSchema):
    """Approval outcome"""
    leave_id: UUID
    status: LeaveStatus

    approved_by: Optional[UUID]
    approved_by_name: Optional[str]
    approved_at: Optional[datetime]

    rejected_by: Optional[UUID]
    rejected_by_name: Optional[str]
    rejected_at: Optional[datetime]

    message: str