"""
Leave response schemas
"""
from datetime import date, datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import LeaveType, LeaveStatus


class LeaveResponse(BaseResponseSchema):
    """Leave list item for basic display"""
    student_id: UUID
    student_name: str
    hostel_id: UUID
    hostel_name: str

    leave_type: LeaveType
    from_date: date
    to_date: date
    total_days: int

    status: LeaveStatus
    applied_at: datetime


class LeaveDetail(BaseResponseSchema):
    """Detailed leave view"""
    student_id: UUID
    student_name: str
    student_room: Optional[str]

    hostel_id: UUID
    hostel_name: str

    leave_type: LeaveType
    from_date: date
    to_date: date
    total_days: int
    reason: str

    contact_during_leave: Optional[str]
    emergency_contact: Optional[str]
    supporting_document_url: Optional[str]

    status: LeaveStatus
    applied_at: datetime
    approved_at: Optional[datetime]
    rejected_at: Optional[datetime]
    cancelled_at: Optional[datetime]

    approved_by: Optional[UUID]
    approved_by_name: Optional[str]
    rejected_by: Optional[UUID]
    rejected_by_name: Optional[str]

    rejection_reason: Optional[str]
    cancellation_reason: Optional[str]


class LeaveListItem(BaseSchema):
    """List row for leave applications"""
    id: UUID
    student_name: str
    room_number: Optional[str]
    leave_type: LeaveType
    from_date: date
    to_date: date
    total_days: int
    status: LeaveStatus
    applied_at: datetime