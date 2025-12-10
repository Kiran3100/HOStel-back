"""
Leave application & cancellation request schemas
"""
from datetime import date
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema
from app.schemas.common.enums import LeaveType


class LeaveApplicationRequest(BaseCreateSchema):
    """Student-sent leave application request"""
    student_id: UUID
    hostel_id: UUID

    leave_type: LeaveType
    from_date: date
    to_date: date
    reason: str = Field(..., min_length=10, max_length=1000)

    contact_during_leave: Optional[str] = Field(None, max_length=20)
    emergency_contact: Optional[str] = Field(None, max_length=20)

    supporting_document_url: Optional[str] = None


class LeaveCancellationRequest(BaseCreateSchema):
    """Student request to cancel an already approved/pending leave"""
    leave_id: UUID
    student_id: UUID

    cancellation_reason: str = Field(..., min_length=10, max_length=500)