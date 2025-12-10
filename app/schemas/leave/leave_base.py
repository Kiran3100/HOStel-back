"""
Base leave schemas
"""
from datetime import date
from typing import Optional
from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseUpdateSchema
from app.schemas.common.enums import LeaveType, LeaveStatus


class LeaveBase(BaseSchema):
    """Base leave application fields"""
    student_id: UUID = Field(..., description="Student requesting leave")
    hostel_id: UUID = Field(..., description="Hostel context")

    leave_type: LeaveType = Field(..., description="Type of leave")
    from_date: date = Field(..., description="Start of leave")
    to_date: date = Field(..., description="End of leave")
    total_days: int = Field(..., ge=1, description="Computed total leave days")

    reason: str = Field(..., min_length=10, max_length=1000, description="Leave reason")

    contact_during_leave: Optional[str] = Field(
        None, max_length=20, description="Contact phone during leave"
    )
    emergency_contact: Optional[str] = Field(
        None, max_length=20, description="Emergency contact during leave"
    )

    supporting_document_url: Optional[str] = Field(
        None, description="Document URL (e.g. medical certificate)"
    )

    @field_validator("total_days")
    @classmethod
    def validate_total_days(cls, v: int, info):
        if "from_date" in info.data and "to_date" in info.data:
            fd = info.data["from_date"]
            td = info.data["to_date"]
            days = (td - fd).days + 1
            if days != v:
                raise ValueError("total_days must equal (to_date - from_date + 1)")
        return v


class LeaveCreate(LeaveBase, BaseCreateSchema):
    """Create leave application"""
    pass


class LeaveUpdate(BaseUpdateSchema):
    """Update leave application (typically before approval)"""
    leave_type: Optional[LeaveType] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    total_days: Optional[int] = Field(None, ge=1)
    reason: Optional[str] = None
    contact_during_leave: Optional[str] = None
    emergency_contact: Optional[str] = None
    supporting_document_url: Optional[str] = None
    status: Optional[LeaveStatus] = None